import React from "react";
import type {
  PropertyResult,
} from "../services/api";
import PropertyCard from "./PropertyCard";
import "./PropertyResults.css";

interface PropertyResultsProps {
  properties: PropertyResult[];
  onAsk: (property: PropertyResult) => void;
}

export default function PropertyResults({
  properties,
  onAsk,
}: PropertyResultsProps) {
  if (!properties.length) {
    return (
      <div className="property-results-empty">
        <div className="empty-icon">🔎</div>

        <h3>No matching properties found</h3>

        <p>
          Try asking for a location, property type,
          or investment preference.
        </p>
      </div>
    );
  }

  return (
    <section className="property-results">
      <div className="property-results-header">
        <div>
          <h3>Properties I found</h3>

          <p>
            {properties.length}{" "}
            {properties.length === 1
              ? "property"
              : "properties"}{" "}
            matching your request
          </p>
        </div>
      </div>

      <div className="property-results-list">
        {properties.map((property, index) => (
          <PropertyCard
            key={
              property.id ??
              property.metadata.property_id ??
              property.metadata.record_id ??
              property.metadata.property_name ??
              property.metadata.source_url ??
              index
            }
            property={property}
            onAsk={onAsk}
          />
        ))}
      </div>
    </section>
  );
}
