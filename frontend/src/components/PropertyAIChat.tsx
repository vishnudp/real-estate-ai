import React, { useState } from "react";
import type {
  PropertyResult,
} from "../services/api";
import { askPropertyAI } from "../services/api";
import PropertyAIAnswer from "./PropertyAIAnswer";
import "./PropertyAIChat.css";

interface PropertyAIChatProps {
  property: PropertyResult;
  onClose: () => void;
}

interface Question {
  query: string;
  answer: string;
}

export default function PropertyAIChat({
  property,
  onClose,
}: PropertyAIChatProps) {
  const [query, setQuery] = useState("");
  const [questions, setQuestions] = useState<
    Question[]
  >([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const metadata = property.metadata;

  const propertyName =
    metadata.property_name ||
    metadata.title ||
    "Selected property";

  const location = [
    metadata.city,
    metadata.country,
  ]
    .filter(Boolean)
    .join(", ");

  async function handleAsk() {
    const trimmedQuery = query.trim();

    if (!trimmedQuery || loading) {
      return;
    }

    if (!property.id) {
      setError(
        "This property does not have a property ID yet."
      );
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await askPropertyAI(
        property.id,
        trimmedQuery
      );

      setQuestions((previous) => [
        ...previous,
        {
          query: trimmedQuery,
          answer: response.answer,
        },
      ]);

      setQuery("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to analyze property."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleSuggestedQuestion(
    question: string
  ) {
    setQuery(question);
  }

  return (
    <section className="property-ai-chat">
      <div className="property-ai-chat-header">
        <div className="property-ai-header-info">
          <div className="property-ai-badge">
            ✦
          </div>

          <div>
            <div className="property-ai-label">
              Property Intelligence
            </div>

            <h2>{propertyName}</h2>

            {location && (
              <div className="property-ai-location">
                📍 {location}
              </div>
            )}
          </div>
        </div>

        <button
          type="button"
          className="property-ai-close"
          onClick={onClose}
          aria-label="Close property intelligence"
        >
          ×
        </button>
      </div>

      <div className="property-ai-context">
        {metadata.developer && (
          <span>
            Developer: {metadata.developer}
          </span>
        )}

        {metadata.brand && (
          <span>
            Brand: {metadata.brand}
          </span>
        )}

        {metadata.location && (
          <span>
            Location: {metadata.location}
          </span>
        )}
      </div>

      {questions.length === 0 && (
        <div className="property-ai-welcome">
          <div className="property-ai-welcome-icon">
            ✦
          </div>

          <h3>
            What would you like to know?
          </h3>

          <p>
            Ask me about investment potential,
            risks, valuation, location, or anything
            else about this property.
          </p>

          <div className="suggested-questions">
            <button
              type="button"
              onClick={() =>
                handleSuggestedQuestion(
                  "Is this property good to buy or are there any risks?"
                )
              }
            >
              Is this property good to buy?
            </button>

            <button
              type="button"
              onClick={() =>
                handleSuggestedQuestion(
                  "What are the main risks of this property?"
                )
              }
            >
              What are the main risks?
            </button>

            <button
              type="button"
              onClick={() =>
                handleSuggestedQuestion(
                  "How attractive is this property as an investment?"
                )
              }
            >
              Is this a good investment?
            </button>

            <button
              type="button"
              onClick={() =>
                handleSuggestedQuestion(
                  "What should I check before buying this property?"
                )
              }
            >
              What should I check?
            </button>
          </div>
        </div>
      )}

      {questions.length > 0 && (
        <div className="property-ai-conversation">
          {questions.map((item, index) => (
            <div
              key={index}
              className="property-ai-turn"
            >
              <div className="property-ai-user-question">
                <span className="question-avatar">
                  You
                </span>

                <div className="question-text">
                  {item.query}
                </div>
              </div>

              <PropertyAIAnswer
                answer={item.answer}
              />
            </div>
          ))}
        </div>
      )}

      {error && (
        <div className="property-ai-error">
          {error}
        </div>
      )}

      <div className="property-ai-input-wrapper">
        <textarea
          value={query}
          onChange={(event) =>
            setQuery(event.target.value)
          }
          onKeyDown={(event) => {
            if (
              event.key === "Enter" &&
              !event.shiftKey
            ) {
              event.preventDefault();
              handleAsk();
            }
          }}
          placeholder="Ask about this property..."
          rows={2}
          disabled={loading}
        />

        <button
          type="button"
          onClick={handleAsk}
          disabled={!query.trim() || loading}
          className="property-ai-send"
        >
          {loading ? (
            <span className="property-ai-spinner" />
          ) : (
            "↑"
          )}
        </button>
      </div>

      <div className="property-ai-input-hint">
        Press Enter to ask · Shift + Enter for a
        new line
      </div>
    </section>
  );
}
