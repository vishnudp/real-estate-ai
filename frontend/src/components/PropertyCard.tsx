import React from "react";
import type { PropertyResult } from "../services/api";
import "./PropertyCard.css";

interface PropertyCardProps {
  property: PropertyResult;
  onAsk: (property: PropertyResult) => void;
}

export default function PropertyCard({
  property,
  onAsk,
}: PropertyCardProps) {
  const metadata = property.metadata || {};

  const propertyName =
    metadata.property_name ||
    metadata.title ||
    "Property opportunity";

  const location = [
    metadata.city,
    metadata.country,
  ]
    .filter(Boolean)
    .join(", ");

  /*
   * Prefer the real database property_id.
   * Fall back to record_id for Chroma-only records.
   */
  const propertyId =
    property.property_id ??
    property.id ??
    metadata.property_id ??
    metadata.record_id ??
    null;

  /*
   * Use the supplied description when available.
   * Otherwise create a short useful description
   * from the available property information.
   */
  const description =
    metadata.description ||
    buildFallbackDescription(metadata);

  return (
    <article className="property-card">

      {/* Property ID */}

      <div className="property-id-row">
        <span className="property-id-label">
          Property ID
        </span>

        <span className="property-id-value">
          {propertyId !== null &&
          propertyId !== undefined &&
          String(propertyId).trim() !== ""
            ? String(propertyId)
            : "N/A"}
        </span>
      </div>

      {/* Property header */}

      <div className="property-card-top">
        <div className="property-card-icon">
          🏠
        </div>

        <div className="property-card-title">
          <h3>{propertyName}</h3>

          {location && (
            <div className="property-location">
              <span>📍</span>
              {location}
            </div>
          )}
        </div>
      </div>

      {/* Tags */}

      <div className="property-tags">
        {metadata.location && (
          <span className="property-tag">
            {metadata.location}
          </span>
        )}

        {metadata.property_type && (
          <span className="property-tag">
            {String(metadata.property_type).replace(
              /_/g,
              " "
            )}
          </span>
        )}

        {metadata.brand && (
          <span className="property-tag brand-tag">
            {metadata.brand}
          </span>
        )}
      </div>

      {/* Developer */}

      {metadata.developer && (
        <div className="property-detail">
          <span>Developer</span>
          <strong>{metadata.developer}</strong>
        </div>
      )}

      {/* Description */}

      <div className="property-description">
        <p>{description}</p>
      </div>

      {/* Footer */}

      <div className="property-card-footer">
        {metadata.source_url && (
          <a
            href={metadata.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="property-link"
          >
            View property
          </a>
        )}

        <button
          type="button"
          className="ask-property-button"
          onClick={() => onAsk(property)}
        >
          Ask about this property
          <span>→</span>
        </button>
      </div>
    </article>
  );
}


/**
 * Creates a useful description when the source record
 * does not contain an explicit description.
 */
function buildFallbackDescription(
  metadata: PropertyResult["metadata"]
): string {
  const parts: string[] = [];

  const propertyType =
    metadata.property_type
      ? String(metadata.property_type).replace(
          /_/g,
          " "
        )
      : "";

  if (propertyType) {
    parts.push(
      `This ${propertyType} property`
    );
  } else {
    parts.push(
      "This property"
    );
  }

  if (metadata.location) {
    parts.push(
      `is located in ${metadata.location}`
    );
  } else if (
    metadata.city ||
    metadata.country
  ) {
    const location = [
      metadata.city,
      metadata.country,
    ]
      .filter(Boolean)
      .join(", ");

    parts.push(
      `is located in ${location}`
    );
  }

  if (metadata.developer) {
    parts.push(
      `and is developed by ${metadata.developer}`
    );
  }

//   if (metadata?.area) {
//     const areaText = metadata?.area_unit
//       ? `${metadata.area} ${metadata?.area_unit}`
//       : String(metadata.area);

//     parts.push(
//       `with an area of ${areaText}`
//     );
//   }

  if (metadata.bedrooms) {
    parts.push(
      `and ${metadata.bedrooms} bedrooms`
    );
  }

  if (parts.length === 1) {
    return (
      "Property details are available from the supplied listing data."
    );
  }

  return `${parts.join(" ")}.`;
}
