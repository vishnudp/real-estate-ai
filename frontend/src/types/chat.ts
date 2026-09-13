import type { PropertyResult } from "./property";

export type ChatMessageRole =
  | "user"
  | "assistant";

export type ChatMessageType =
  | "text"
  | "properties"
  | "property-ai";

export interface ChatMessage {
  id: string;
  role: ChatMessageRole;
  type: ChatMessageType;
  content?: string;
  properties?: PropertyResult[];
}
