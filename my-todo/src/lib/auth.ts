import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "./db";
import * as schema from "@/db/schema";

export const auth = betterAuth({
    database: drizzleAdapter(db, {
        provider: "pg",
        schema: {
            user: schema.users,
            session: schema.sessions,
            account: schema.accounts,
            verification: schema.verifications,
        },
    }),
    emailAndPassword: {
        enabled: true
    },
    session: {
        expiresIn: 60 * 60 * 24 * 7, // 7 days
        updateAge: 60 * 60 * 24, // 1 day
    },
    // Cookie configuration for localhost development
    advanced: {
        cookies: {
            session_token: {
                name: "better-auth.session_token",
                attributes: {
                    sameSite: "lax",
                    secure: false, // false for localhost (http)
                    path: "/",
                    httpOnly: true,
                },
            },
        },
    },
});