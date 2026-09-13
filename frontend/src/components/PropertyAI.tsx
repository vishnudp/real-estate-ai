import {
  useState,
} from "react";

import PropertyAIAnswer from "./PropertyAIAnswer";

import {
  askPropertyAI,
} from "../services/propertyAI";

interface PropertyAIProps {
  propertyId: number;
}

export default function PropertyAI({
  propertyId,
}: PropertyAIProps) {
  const [
    query,
    setQuery,
  ] = useState(
    "Is this property a good investment and what are the main concerns?",
  );

  const [
    answer,
    setAnswer,
  ] = useState("");

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");

  async function handleAsk() {
    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response =
        await askPropertyAI(
          propertyId,
          query,
        );

      setAnswer(response.answer);

    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to analyze property.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="property-ai">
      <h2>
        AI Investment Analysis
      </h2>

      <textarea
        value={query}
        onChange={(event) =>
          setQuery(event.target.value)
        }
        rows={4}
        placeholder="Ask about this property..."
      />

      <button
        type="button"
        onClick={handleAsk}
        disabled={
          loading ||
          !query.trim()
        }
      >
        {loading
          ? "Analyzing..."
          : "Ask AI"}
      </button>

      {error && (
        <div className="ai-error">
          {error}
        </div>
      )}

      {answer && (
        <PropertyAIAnswer
          answer={answer}
        />
      )}
    </div>
  );
}
