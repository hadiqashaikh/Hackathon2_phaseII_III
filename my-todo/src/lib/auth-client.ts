import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
    fetchOptions: {
        credentials: 'include',
    },
    // Explicitly enable cookie storage
    fetch: async (url, options) => {
        const response = await fetch(url, {
            ...options,
            credentials: 'include',
        });
        return response;
    },
});