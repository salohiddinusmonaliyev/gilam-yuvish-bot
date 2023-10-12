from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())


    async def add_user(self, full_name, telegram_id):
        sql = "INSERT INTO base_customuser (full_name, telegram_id) VALUES($1, $2) returning *"
        return await self.execute(sql, full_name, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM base_customuser"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM base_customuser WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def drop_users(self):
        await self.execute("DROP TABLE base_customuser", execute=True)

    async def add_invoice(self, invoice, order_number):
        sql = "INSERT INTO base_invoice (order_number,invoice) VALUES($1, $2) returning *"
        return await self.execute(sql, order_number, invoice, fetchrow=True)

    async def add_order(
            self,
            user_id,
            address,
            service_id,
            phone_number,
            delivered,
            is_completed,
            supplier_id,
            price
    ):

        # sql = "INSERT INTO base_order (user_id, address, service_id, invoice, phone_number, delivered, is_completed, supplier_id, price) VALUES($1, $2, $3, $4, $5, $6, $7, $8) returning *"
        sql = "INSERT INTO base_order (user_id, address, service_id, phone_number, delivered, is_completed,supplier_id, price) VALUES($1, $2, $3, $4, $5, $6, $7, $8) returning *"

        return await self.execute(
            sql,
            user_id,
            address,
            service_id,
            phone_number,
            delivered,
            is_completed,
            supplier_id,
            price,
            fetchrow=True,
        )

    async def get_orders(self, user_id):
        sql = f"""SELECT base_order.*
                FROM base_order
                JOIN base_customuser ON base_order.user_id = base_customuser.id
                WHERE base_customuser.telegram_id = {user_id} ORDER BY id DESC ;
"""
        return await self.execute(sql, fetch=True)

    async def get_all_orders(self):
        sql = f"""SELECT base_order.*
                FROM base_order
                JOIN base_customuser ON base_order.user_id = base_customuser.id
                ORDER BY id DESC ;
"""
        return await self.execute(sql, fetch=True)

    async def get_services(self):
        sql = f"SELECT * FROM base_service"
        return await self.execute(sql, fetch=True)


    async def get_order(self, id):
        sql = f"SELECT * FROM base_order WHERE id={id}"
        return await self.execute(sql, fetchrow=True)


    async def get_invoice(self, id):
        sql = f"SELECT * FROM base_invoice WHERE order_number=CAST({id} AS integer);"
        return await self.execute(sql, fetchrow=True)

    async def get_service(self, id):
        sql = f"SELECT * FROM base_service WHERE id={id}"
        return await self.execute(sql, fetch=True)

    async def completed(self, id):
        sql = f"""
        UPDATE base_order
        SET is_completed = TRUE
        WHERE id = $1;
        """
        return await self.execute(sql,id, execute=True)

    async def delivered(self, id, supplier):
        sql = f"""
        UPDATE base_order
        SET delivered = TRUE, supplier_id = $2
        WHERE id = $1;
        """
        return await self.execute(sql, id, supplier, execute=True)

    async def update_price(self, id, price):
        sql = f"""
        UPDATE base_order
        SET price = {price}
        WHERE id = $1;
        """
        return await self.execute(sql, id, execute=True)
        

    async def update_invoice(self, id, file_id):
        sql = """
        UPDATE base_invoice
        SET invoice = $2
        WHERE order_number = $1;
        """
        return await self.execute(sql, id, file_id, execute=True)

    async def update_count(self, id):
        sql = f"""
        UPDATE base_customuser
        SET count = count + 1
        WHERE id = $1;
        """
        return await self.execute(sql, id, execute=True)
        
    async def delete_invoice(self, id):
        sql = f"""
        DELETE FROM base_invoice
        WHERE order_number = $1;
        """
        return await self.execute(sql, id, execute=True)
