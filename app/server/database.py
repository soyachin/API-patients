import motor.motor_asyncio
import os, logging
import pytz
from datetime import datetime

def convert_to_peru_timezone(dt: datetime) -> datetime:
    peru_tz = pytz.timezone('America/Lima')
    return dt.astimezone(peru_tz)

mongo_uri = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
database = client.P1pacientes_test
collection = database.get_collection("Pacientes")

# GET ALL
async def retrieve_pacientes():
    pacientes = []
    async for paciente in collection.find():
        pacientes.append(paciente)
    return pacientes

# PUT
async def insert_paciente(data: dict):
    paciente = await collection.insert_one(data)
    new_paciente = await collection.find_one({"_id": paciente.inserted_id})
    return new_paciente


# GET BY ID
async def retrieve_paciente_by_id(id: str):
    paciente = await collection.find_one({"_id": id})
    if paciente:
        return paciente


# UPDATE
async def modify_paciente(id: str, data: dict):
    if len(data) < 1:
        return False
    paciente = await collection.find_one({"_id": id})
    if paciente:
        try:
            if 'fecha_nacimiento' in data:
                data['fecha_nacimiento'] = convert_to_peru_timezone(data['fecha_nacimiento'])
            if 'seguro' in data and 'vencimiento' in data['seguro']:
                data['seguro']['vencimiento'] = convert_to_peru_timezone(data['seguro']['vencimiento'])


            updated_paciente = await collection.update_one(
                {"_id": id}, {"$set": data}
            )
            if updated_paciente.modified_count > 0:
                return True
            return False
        except Exception as e:
            logging.error(f"Error actualizando paciente: {e}")
            raise e

# DELETE
async def remove_paciente(id: str):
    student = await collection.find_one({"_id": id})
    if student:
        await collection.delete_one({"_id": id})
        return True
    return False


