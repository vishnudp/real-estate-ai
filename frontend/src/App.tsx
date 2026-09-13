import {
  useState,
} from "react";

import {
  searchProperties,
} from "./services/api";

import type {
  PropertyResult,
} from "./types/property";

import type {
  ChatMessage,
} from "./types/chat";

import PropertyCard from "./components/PropertyCard";

import PropertyAIChat from "./components/PropertyAIChat";

import "./App.css";

function createId() {
  return `${Date.now()}-${Math.random()
    .toString(36)
    .slice(2)}`;
}

export default function App() {
  const [messages, setMessages] =
    useState<ChatMessage[]>([]);

  const [input, setInput] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [selectedProperty, setSelectedProperty] =
    useState<PropertyResult | null>(
      null
    );

  async function handleSearch() {
    const query =
      input.trim();

    if (!query || loading) {
      return;
    }

    setInput("");

    const userMessage: ChatMessage = {
      id: createId(),
      role: "user",
      type: "text",
      content: query,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setLoading(true);

    try {
      const response =
        await searchProperties(
          query,
          20
        );

      const assistantMessage: ChatMessage = {
        id: createId(),
        role: "assistant",
        type: "properties",
        content:
          response.results.length
            ? `I found ${response.results.length} properties matching your request.`
            : "I couldn't find matching properties.",
        properties:
          response.results,
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);
    } catch (error) {
      const assistantMessage: ChatMessage = {
        id: createId(),
        role: "assistant",
        type: "text",
        content:
          error instanceof Error
            ? error.message
            : "Unable to search properties.",
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleAskProperty(
    property: PropertyResult
  ) {
    setSelectedProperty(property);
  }

  return (
    <div className="app">
      <div className="chat-container">

        <header className="chat-header">
          <div>
            <div className="brand-label">
              REAL ESTATE AI
            </div>

            <h1>
              Property Intelligence
            </h1>

            <p>
              Find properties and ask
              intelligent questions about
              them.
            </p>
          </div>
        </header>

        <main className="chat-content">

          {messages.length === 0 && (
            <div className="welcome">
              <h2>
                What property are you
                looking for?
              </h2>

              <p>
                Try asking something like:
              </p>

              <button
                onClick={() =>
                  setInput(
                    "Please share me the property in Oman"
                  )
                }
              >
                Please share me the property
                in Oman
              </button>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${
                message.role
              }`}
            >
              {message.role ===
                "assistant" && (
                <div className="assistant-label">
                  AI
                </div>
              )}

              {message.content && (
                <div className="message-text">
                  {message.content}
                </div>
              )}

              {message.type ===
                "properties" &&
                message.properties && (
                  <div className="property-results">
                    {message.properties.map(
                      (
                        property,
                        index
                      ) => (
                        <PropertyCard
                          key={
                            property.id ??
                            property.metadata
                              .property_name ??
                            property.metadata
                              .source_url ??
                            index
                          }
                          property={
                            property
                          }
                          onAsk={
                            handleAskProperty
                          }
                        />
                      )
                    )}
                  </div>
                )}
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="assistant-label">
                AI
              </div>

              <div className="loading">
                Searching properties...
              </div>
            </div>
          )}

          {selectedProperty && (
            <PropertyAIChat
              property={
                selectedProperty
              }
              onClose={() =>
                setSelectedProperty(
                  null
                )
              }
            />
          )}
        </main>

        <div className="chat-input-container">
          <input
            value={input}
            onChange={(event) =>
              setInput(
                event.target.value
              )
            }
            onKeyDown={(event) => {
              if (
                event.key === "Enter"
              ) {
                handleSearch();
              }
            }}
            placeholder="Ask for properties..."
            disabled={loading}
          />

          <button
            onClick={handleSearch}
            disabled={
              loading ||
              !input.trim()
            }
          >
            {loading
              ? "Searching..."
              : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
