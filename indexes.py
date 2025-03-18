

Índice para busca rápida de pacientes pelo CPF

patients_collection.create_index("cpf", unique=True)

Garante que não haja CPFs duplicados e acelera consultas como:

paciente = patients_collection.find_one({"cpf": "123.456.789-00"})
--------------------------------------

Índice para melhorar a performance em busca de agendamentos

appointments_collection.create_index([("paciente_id", 1), ("data_agendamento", -1)])

Ajuda a encontrar rapidamente os agendamentos de um paciente e ordená-los pela data (do mais recente para o mais antigo):

agendamentos = appointments_collection.find({"paciente_id": patient_data["_id"]}).sort("data_agendamento", -1)

--------------------------------------

Para busca eficiente de vacinas pelo nome

vaccines_collection.create_index("nome")

Facilita a recuperação de dados de uma vacina específica:

vacina = vaccines_collection.find_one({"nome": "COVID-19"} )
