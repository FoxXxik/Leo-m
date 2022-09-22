import aiosqlite


class TeleData:

    def __init__(self, db_file):
        self.base = db_file

    async def is_user_exists(self, tele_id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT id FROM users WHERE tele_id = ?", (tele_id,)) as cursor:
                result = await cursor.fetchall()
                await cursor.close()
                return bool(len(result))

    async def add_user(self, tele_id):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("INSERT INTO users ('tele_id') VALUES (?)", (tele_id,))
            await connect.commit()

    async def add_request(self, tele_id, text, docs, photos, contact, IE, name, req_type):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("INSERT INTO requests ('tele_id', 'checker', 'text', 'docs', 'photos', 'contact', 'IE', 'name', 'r_type') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (tele_id, 1, text, docs, photos, contact, IE, name, req_type))
            await connect.commit()

    async def disable_checker(self, tele_id):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("UPDATE requests SET checker = 0 WHERE tele_id = ?", (tele_id,))
            await connect.commit()

    async def get_request_id(self, tele_id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT id FROM requests WHERE tele_id = ? AND checker = 1", (tele_id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return result

    async def is_admin(self, tele_id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT is_admin FROM users WHERE tele_id = ?", (tele_id,)) as cursor:
                result = await cursor.fetchall()
                await cursor.close()
                return bool(list(result)[0])

    async def set_admin(self, tele_id):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("UPDATE users SET is_admin = 1 WHERE tele_id = ?", (tele_id,))
            await connect.commit()

    async def is_request_exists(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT tele_id FROM requests WHERE id = ? AND is_finished = 0", (id,)) as cursor:
                result = await cursor.fetchall()
                await cursor.close()
                return bool(len(result))

    async def get_tele_id(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT tele_id FROM requests WHERE id = ?", (id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return list(result)[0]

    async def finish_req(self, id):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("UPDATE requests SET is_finished = 1 WHERE id = ?", (id, ))
            await connect.commit()

    async def get_status(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT is_finished FROM requests WHERE id = ?", (id,)) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return list(result)[0]

    async def get_text(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT text FROM requests WHERE id = ?", (id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return list(result)[0]

    async def get_docs(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT docs FROM requests WHERE id = ?", (id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return list(result)[0]

    async def get_photos(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT photos FROM requests WHERE id = ?", (id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return list(result)[0]

    async def get_contact(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT contact FROM requests WHERE id = ?", (id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return list(result)[0]

    async def get_IE(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT IE FROM requests WHERE id = ?", (id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return list(result)[0]

    async def get_name(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT name FROM requests WHERE id = ?", (id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return list(result)[0]

    async def get_type(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT r_type FROM requests WHERE id = ?", (id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return list(result)[0]

    async def is_archive_req(self, id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT tele_id FROM requests WHERE id = ?", (id, )) as cursor:
                result = await cursor.fetchall()
                await cursor.close()
                return bool(len(result))