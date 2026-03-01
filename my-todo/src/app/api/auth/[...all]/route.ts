import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js"; // Yahan tabdeeli ki hai

export const { POST, GET } = toNextJsHandler(auth);