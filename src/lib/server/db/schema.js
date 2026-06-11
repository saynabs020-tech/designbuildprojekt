import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';

export const user = sqliteTable('user', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    username: text('username').notNull().unique(),
    password: text('password').notNull(),
    role: text('role').notNull() // Gemmer 'patient' eller 'healthcare'
});