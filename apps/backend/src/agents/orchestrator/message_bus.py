"""
Message Bus for Inter-Agent Communication

This module provides a simple message bus for communication between agents
in the Eco-Shift system. It supports publish-subscribe pattern and message queuing.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import uuid


logger = logging.getLogger(__name__)


class MessagePriority(Enum):
    """Message priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class MessageType(Enum):
    """Types of messages that can be sent between agents"""
    WEATHER_ALERT = "weather_alert"
    VENDOR_LIST = "vendor_list"
    AUDIT_REQUEST = "audit_request"
    AUDIT_RESULT = "audit_result"
    OPTIMIZATION_REQUEST = "optimization_request"
    OPTIMIZATION_RESULT = "optimization_result"
    AGENT_STATUS = "agent_status"
    ERROR = "error"
    COMMAND = "command"


@dataclass
class Message:
    """Represents a message in the system"""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType = MessageType.COMMAND
    sender: str = ""
    recipient: Optional[str] = None  # None means broadcast
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.utcnow)
    ttl: Optional[int] = None  # Time-to-live in seconds
    correlation_id: Optional[str] = None  # For request-response patterns
    
    def is_expired(self) -> bool:
        """Check if the message has expired"""
        if self.ttl is None:
            return False
        expiry_time = self.timestamp + timedelta(seconds=self.ttl)
        return datetime.utcnow() > expiry_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "sender": self.sender,
            "recipient": self.recipient,
            "payload": self.payload,
            "priority": self.priority.value,
            "timestamp": self.timestamp.isoformat(),
            "ttl": self.ttl,
            "correlation_id": self.correlation_id
        }


class MessageBus:
    """
    Simple message bus for inter-agent communication.
    
    Supports:
    - Publish-subscribe pattern
    - Message queuing
    - Priority-based delivery
    - Message expiration
    - Request-response patterns
    """
    
    def __init__(self, max_queue_size: int = 1000, default_ttl: int = 3600):
        self.max_queue_size = max_queue_size
        self.default_ttl = default_ttl
        
        # Subscribers: topic -> list of callback functions
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        
        # Message queues: agent_id -> priority queue
        self._queues: Dict[str, asyncio.PriorityQueue] = {}
        
        # Pending responses: correlation_id -> Future
        self._pending_responses: Dict[str, asyncio.Future] = {}
        
        # Message history for debugging
        self._message_history: List[Message] = []
        self._max_history = 100
        
        self._running = False
        self._cleanup_task: Optional[asyncio.Task] = None
        
        logger.info("Message bus initialized")
    
    async def start(self):
        """Start the message bus"""
        if self._running:
            logger.warning("Message bus already running")
            return
        
        self._running = True
        self._cleanup_task = asyncio.create_task(self._cleanup_expired_messages())
        logger.info("Message bus started")
    
    async def stop(self):
        """Stop the message bus"""
        if not self._running:
            return
        
        self._running = False
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Message bus stopped")
    
    def subscribe(self, topic: str, callback: Callable):
        """
        Subscribe to a topic
        
        Args:
            topic: Topic to subscribe to (e.g., "weather_alert", "audit_result")
            callback: Async function to call when message is received
        """
        self._subscribers[topic].append(callback)
        logger.debug(f"Subscribed to topic: {topic}")
    
    def unsubscribe(self, topic: str, callback: Callable):
        """Unsubscribe from a topic"""
        if topic in self._subscribers and callback in self._subscribers[topic]:
            self._subscribers[topic].remove(callback)
            logger.debug(f"Unsubscribed from topic: {topic}")
    
    async def publish(self, message: Message):
        """
        Publish a message to all subscribers of its type
        
        Args:
            message: Message to publish
        """
        if message.is_expired():
            logger.warning(f"Attempted to publish expired message: {message.id}")
            return
        
        # Set default TTL if not specified
        if message.ttl is None:
            message.ttl = self.default_ttl
        
        # Add to history
        self._add_to_history(message)
        
        # Get topic from message type
        topic = message.type.value
        
        # Publish to subscribers
        if topic in self._subscribers:
            logger.debug(f"Publishing message {message.id} to {len(self._subscribers[topic])} subscribers")
            for callback in self._subscribers[topic]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(message)
                    else:
                        callback(message)
                except Exception as e:
                    logger.error(f"Error in subscriber callback: {e}", exc_info=True)
        
        # If message has a specific recipient, add to their queue
        if message.recipient:
            await self._enqueue_message(message.recipient, message)
    
    async def send(self, message: Message):
        """
        Send a message directly to a recipient's queue
        
        Args:
            message: Message to send
        """
        if not message.recipient:
            raise ValueError("Message must have a recipient for direct send")
        
        if message.ttl is None:
            message.ttl = self.default_ttl
        
        self._add_to_history(message)
        await self._enqueue_message(message.recipient, message)
    
    async def request(self, message: Message, timeout: float = 30.0) -> Message:
        """
        Send a request and wait for a response
        
        Args:
            message: Request message
            timeout: Timeout in seconds
            
        Returns:
            Response message
        """
        if not message.correlation_id:
            message.correlation_id = str(uuid.uuid4())
        
        # Create a future for the response
        future = asyncio.Future()
        self._pending_responses[message.correlation_id] = future
        
        try:
            # Send the request
            await self.publish(message)
            
            # Wait for response with timeout
            response = await asyncio.wait_for(future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            logger.error(f"Request {message.correlation_id} timed out")
            raise
        finally:
            # Clean up
            self._pending_responses.pop(message.correlation_id, None)
    
    async def respond(self, request_message: Message, response_payload: Dict[str, Any]):
        """
        Send a response to a request
        
        Args:
            request_message: Original request message
            response_payload: Response data
        """
        if not request_message.correlation_id:
            logger.warning("Cannot respond to message without correlation_id")
            return
        
        response = Message(
            type=request_message.type,
            sender=request_message.recipient or "unknown",
            recipient=request_message.sender,
            payload=response_payload,
            correlation_id=request_message.correlation_id
        )
        
        # If there's a pending future, resolve it
        if request_message.correlation_id in self._pending_responses:
            future = self._pending_responses[request_message.correlation_id]
            if not future.done():
                future.set_result(response)
        else:
            # Otherwise, just publish the response
            await self.publish(response)
    
    async def receive(self, agent_id: str, timeout: Optional[float] = None) -> Optional[Message]:
        """
        Receive a message from an agent's queue
        
        Args:
            agent_id: Agent identifier
            timeout: Optional timeout in seconds
            
        Returns:
            Message or None if timeout
        """
        if agent_id not in self._queues:
            self._queues[agent_id] = asyncio.PriorityQueue(maxsize=self.max_queue_size)
        
        try:
            if timeout:
                priority, message = await asyncio.wait_for(
                    self._queues[agent_id].get(),
                    timeout=timeout
                )
            else:
                priority, message = await self._queues[agent_id].get()
            
            return message
        except asyncio.TimeoutError:
            return None
    
    async def _enqueue_message(self, agent_id: str, message: Message):
        """Add a message to an agent's queue"""
        if agent_id not in self._queues:
            self._queues[agent_id] = asyncio.PriorityQueue(maxsize=self.max_queue_size)
        
        # Use negative priority for correct ordering (higher priority first)
        priority = -message.priority.value
        
        try:
            await self._queues[agent_id].put((priority, message))
            logger.debug(f"Enqueued message {message.id} for {agent_id}")
        except asyncio.QueueFull:
            logger.error(f"Queue full for agent {agent_id}, dropping message {message.id}")
    
    def _add_to_history(self, message: Message):
        """Add message to history"""
        self._message_history.append(message)
        if len(self._message_history) > self._max_history:
            self._message_history.pop(0)
    
    async def _cleanup_expired_messages(self):
        """Periodically clean up expired messages"""
        while self._running:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                # Clean up message history
                self._message_history = [
                    msg for msg in self._message_history
                    if not msg.is_expired()
                ]
                
                logger.debug("Cleaned up expired messages")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}", exc_info=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get message bus statistics"""
        return {
            "running": self._running,
            "subscribers": {topic: len(callbacks) for topic, callbacks in self._subscribers.items()},
            "queues": {agent_id: queue.qsize() for agent_id, queue in self._queues.items()},
            "pending_responses": len(self._pending_responses),
            "message_history_size": len(self._message_history)
        }
    
    def get_message_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent message history"""
        return [msg.to_dict() for msg in self._message_history[-limit:]]


# Global message bus instance
_message_bus: Optional[MessageBus] = None


def get_message_bus() -> MessageBus:
    """Get the global message bus instance"""
    global _message_bus
    if _message_bus is None:
        _message_bus = MessageBus()
    return _message_bus


async def initialize_message_bus(max_queue_size: int = 1000, default_ttl: int = 3600):
    """Initialize and start the global message bus"""
    global _message_bus
    _message_bus = MessageBus(max_queue_size=max_queue_size, default_ttl=default_ttl)
    await _message_bus.start()
    return _message_bus


async def shutdown_message_bus():
    """Shutdown the global message bus"""
    global _message_bus
    if _message_bus:
        await _message_bus.stop()
        _message_bus = None

# Made with Bob
