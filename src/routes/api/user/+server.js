import { db } from '$lib/server/db';
import { user } from '$lib/server/db/schema.js';
import bcrypt from 'bcryptjs';

export async function POST({ request }) {
	const { username, password,role } = await request.json();
	// validering stopper hvis rolle mangler
	if (!role) {
		return new Response(JSON.stringify({ error: 'Rolle er påkrævet' }), { status: 400 });
	}
	const hashedPass = await bcrypt.hash(password, 10); // Hash the password with bcrypt
	const createduser = await db.insert(user).values({ username, password: hashedPass, role:role }).returning();
	return new Response(JSON.stringify(createduser), { status: 201 }); // HTTP Created
}
