import React from "react";
import "./PropertyAIAnswer.css";

interface PropertyAIAnswerProps {
  answer: string;
}

type Sections = {
  Assessment?: string[];
  Why?: string[];
  "Main concerns"?: string[];
  Valuation?: string[];
  Confidence?: string[];
  Risk?: string[];
};

const SECTION_NAMES = [
  "Assessment",
  "Why",
  "Main concerns",
  "Valuation",
  "Confidence",
  "Risk",
] as const;

function parseAnswer(answer: string): Sections {
  const sections: Sections = {};

  let currentSection:
    | keyof Sections
    | null = null;

  answer.split("\n").forEach((line) => {
    const trimmed = line.trim();

    if (!trimmed) {
      return;
    }

    const matchedSection = SECTION_NAMES.find(
      (section) =>
        trimmed.toLowerCase() ===
        `${section.toLowerCase()}:`
    );

    if (matchedSection) {
      currentSection = matchedSection;
      sections[matchedSection] = [];
      return;
    }

    if (currentSection) {
      sections[currentSection]?.push(trimmed);
    }
  });

  return sections;
}

interface SectionProps {
  title: string;
  children: React.ReactNode;
}

function Section({
  title,
  children,
}: SectionProps) {
  return (
    <section className="ai-answer-section">
      <h3>{title}</h3>
      {children}
    </section>
  );
}

interface LinesProps {
  lines?: string[];
}

function Lines({ lines }: LinesProps) {
  if (!lines?.length) {
    return null;
  }

  return (
    <div className="ai-answer-lines">
      {lines.map((line, index) => {
        const isBullet =
          line.startsWith("- ") ||
          line.startsWith("• ");

        if (isBullet) {
          return (
            <div
              key={index}
              className="ai-answer-bullet"
            >
              <span className="ai-answer-bullet-icon">
                •
              </span>

              <span>
                {line.replace(/^[-•]\s*/, "")}
              </span>
            </div>
          );
        }

        return (
          <p key={index}>
            {line}
          </p>
        );
      })}
    </div>
  );
}

function DirectAnswer({
  answer,
}: {
  answer: string;
}) {
  const lines = answer
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  return (
    <div className="ai-direct-answer">
      {lines.map((line, index) => {

        if (
          line.toLowerCase() === "key risks:"
        ) {
          return (
            <h4
              key={index}
              className="ai-direct-heading"
            >
              Key risks
            </h4>
          );
        }

        const isBullet =
          line.startsWith("- ") ||
          line.startsWith("• ");

        if (isBullet) {
          return (
            <div
              key={index}
              className="ai-answer-bullet"
            >
              <span className="ai-answer-bullet-icon">
                •
              </span>

              <span>
                {line.replace(/^[-•]\s*/, "")}
              </span>
            </div>
          );
        }

        if (
          line.toLowerCase().startsWith(
            "risk level:"
          )
        ) {
          const value = line.substring(
            "risk level:".length
          ).trim();

          return (
            <div
              key={index}
              className="ai-risk-summary"
            >
              <span className="ai-risk-label">
                Risk level
              </span>

              <strong className="ai-risk-value">
                {value}
              </strong>
            </div>
          );
        }

        if (
          line.toLowerCase().startsWith(
            "risk score:"
          )
        ) {
          const value = line.substring(
            "risk score:".length
          ).trim();

          return (
            <div
              key={index}
              className="ai-risk-summary"
            >
              <span className="ai-risk-label">
                Risk Score
              </span>

              <strong className="ai-risk-value">
                {value}
              </strong>
            </div>
          );
        }

        return (
          <p key={index}>
            {line}
          </p>
        );
      })}
    </div>
  );
}

export default function PropertyAIAnswer({
  answer,
}: PropertyAIAnswerProps) {

  if (!answer) {
    return null;
  }

  const sections = parseAnswer(answer);

  const hasStructuredSections =
    Object.keys(sections).length > 0;

  /*
   * Direct factual/risk answers do not use the
   * Assessment / Why / Valuation structure.
   *
   * Render them directly instead of forcing them
   * into the investment-analysis UI.
   */
  if (!hasStructuredSections) {
    return (
      <div className="property-ai-answer">
        <Section title="">
          <DirectAnswer answer={answer} />
        </Section>
      </div>
    );
  }

  return (
    <div className="property-ai-answer">

      {sections.Assessment && (
        <Section title="Assessment">
          <Lines
            lines={sections.Assessment}
          />
        </Section>
      )}

      {sections.Why && (
        <Section title="Why">
          <Lines
            lines={sections.Why}
          />
        </Section>
      )}

      {sections["Main concerns"] && (
        <Section title="Main concerns">
          <Lines
            lines={sections["Main concerns"]}
          />
        </Section>
      )}

      {sections.Risk && (
        <Section title="Risk">
          <Lines
            lines={sections.Risk}
          />
        </Section>
      )}

      {sections.Valuation && (
        <Section title="Valuation">
          <Lines
            lines={sections.Valuation}
          />
        </Section>
      )}

      {sections.Confidence && (
        <Section title="Confidence">
          <Lines
            lines={sections.Confidence}
          />
        </Section>
      )}
    </div>
  );
}
