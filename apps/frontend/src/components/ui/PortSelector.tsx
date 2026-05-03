"use client";

import React, { useState, useRef, useEffect } from "react";
import { Port, searchPorts } from "@/data/world-ports";

interface PortSelectorProps {
  label: string;
  value: Port | null;
  onChange: (port: Port | null) => void;
  placeholder?: string;
  className?: string;
}

export const PortSelector: React.FC<PortSelectorProps> = ({
  label,
  value,
  onChange,
  placeholder = "Search by port name, city, or country...",
  className = "",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredPorts, setFilteredPorts] = useState<Port[]>([]);
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Update search query when value changes externally
  useEffect(() => {
    if (value) {
      setSearchQuery(`${value.name} (${value.code})`);
    } else {
      setSearchQuery("");
    }
  }, [value]);

  // Filter ports based on search query
  useEffect(() => {
    if (searchQuery.trim()) {
      const results = searchPorts(searchQuery);
      setFilteredPorts(results.slice(0, 10)); // Limit to 10 results
      setHighlightedIndex(0);
    } else {
      setFilteredPorts([]);
    }
  }, [searchQuery]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Scroll highlighted item into view
  useEffect(() => {
    if (dropdownRef.current && isOpen) {
      const highlightedElement = dropdownRef.current.children[
        highlightedIndex
      ] as HTMLElement;
      if (highlightedElement) {
        highlightedElement.scrollIntoView({
          block: "nearest",
          behavior: "smooth",
        });
      }
    }
  }, [highlightedIndex, isOpen]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    setIsOpen(true);
    if (!query.trim()) {
      onChange(null);
    }
  };

  const handleInputFocus = () => {
    setIsOpen(true);
  };

  const handlePortSelect = (port: Port) => {
    onChange(port);
    setSearchQuery(`${port.name} (${port.code})`);
    setIsOpen(false);
    inputRef.current?.blur();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!isOpen) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        setIsOpen(true);
        e.preventDefault();
      }
      return;
    }

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setHighlightedIndex((prev) =>
          prev < filteredPorts.length - 1 ? prev + 1 : prev
        );
        break;
      case "ArrowUp":
        e.preventDefault();
        setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : 0));
        break;
      case "Enter":
        e.preventDefault();
        if (filteredPorts[highlightedIndex]) {
          handlePortSelect(filteredPorts[highlightedIndex]);
        }
        break;
      case "Escape":
        e.preventDefault();
        setIsOpen(false);
        inputRef.current?.blur();
        break;
      case "Tab":
        setIsOpen(false);
        break;
    }
  };

  const handleClear = () => {
    setSearchQuery("");
    onChange(null);
    setIsOpen(false);
    inputRef.current?.focus();
  };

  return (
    <div ref={containerRef} className={`relative ${className}`}>
      {/* Label */}
      <label className="block text-sm font-medium text-gray-300 mb-2">
        {label}
      </label>

      {/* Input Container */}
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={searchQuery}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          autoComplete="off"
          aria-label={label}
          aria-autocomplete="list"
          aria-controls="port-dropdown"
          aria-expanded={isOpen}
        />

        {/* Clear Button */}
        {searchQuery && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
            aria-label="Clear selection"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        )}

        {/* Dropdown Icon */}
        {!searchQuery && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </div>
        )}
      </div>

      {/* Dropdown */}
      {isOpen && filteredPorts.length > 0 && (
        <div
          id="port-dropdown"
          ref={dropdownRef}
          className="absolute z-50 w-full mt-2 bg-gray-800 border border-gray-700 rounded-lg shadow-2xl max-h-80 overflow-y-auto"
          role="listbox"
        >
          {filteredPorts.map((port, index) => (
            <button
              key={port.id}
              type="button"
              onClick={() => handlePortSelect(port)}
              onMouseEnter={() => setHighlightedIndex(index)}
              className={`w-full px-4 py-3 text-left transition-colors ${
                index === highlightedIndex
                  ? "bg-blue-600 text-white"
                  : "text-gray-300 hover:bg-gray-700"
              } ${index !== 0 ? "border-t border-gray-700" : ""}`}
              role="option"
              aria-selected={index === highlightedIndex}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="font-medium truncate">{port.name}</div>
                  <div className="text-sm opacity-75 truncate">
                    {port.city}, {port.country}
                  </div>
                </div>
                <div className="ml-3 flex-shrink-0">
                  <span
                    className={`inline-block px-2 py-1 text-xs font-mono rounded ${
                      index === highlightedIndex
                        ? "bg-blue-700"
                        : "bg-gray-700"
                    }`}
                  >
                    {port.code}
                  </span>
                </div>
              </div>
              <div className="text-xs opacity-60 mt-1">{port.region}</div>
            </button>
          ))}
        </div>
      )}

      {/* No Results Message */}
      {isOpen && searchQuery && filteredPorts.length === 0 && (
        <div className="absolute z-50 w-full mt-2 bg-gray-800 border border-gray-700 rounded-lg shadow-2xl p-4 text-center text-gray-400">
          No ports found matching "{searchQuery}"
        </div>
      )}

      {/* Selected Port Info */}
      {value && !isOpen && (
        <div className="mt-2 text-sm text-gray-400">
          <span className="inline-flex items-center gap-2">
            <svg
              className="w-4 h-4 text-green-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            {value.city}, {value.country} • {value.region}
          </span>
        </div>
      )}
    </div>
  );
};

export default PortSelector;

// Made with Bob
