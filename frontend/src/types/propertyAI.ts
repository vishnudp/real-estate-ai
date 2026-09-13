export interface PropertyAIGuardrails {
  passed: boolean;
  fallback_used: boolean;
  violations: string[];
}

export interface PropertyAIResponse {
  intent: string;
  answer: string;
  model: string;
  guardrails: PropertyAIGuardrails;
}
