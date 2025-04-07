from models.task import Task
from flask import Flask, jsonify, request

app = Flask(__name__)

# CRUD
# Create, Read, Update, Delete = Criar, Ler, Atualizar, Deletar
# Tabela: tarefas

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_tasks():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control ,title=data.get("title"), description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso!"}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    # for task in tasks:
    #     task_list.append(task.to_dict())
    output = {
                "taks": task_list,
                "total_tasks": len(task_list),
            }
    return jsonify(output), 200

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    return jsonify({"error": "Tarefa não encontrada!"}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    for task in tasks:
        if task.id == id:
            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.completed = data.get("completed", task.completed)
            return jsonify({"message": "Tarefa atualizada com sucesso!"}), 200
    return jsonify({"error": "Tarefa não encontrada!"}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    task_exists = any(task.id == id for task in tasks)

    if not task_exists:
        return jsonify({"error": "Tarefa não encontrada!"}), 404
    tasks = [task for task in tasks if task.id != id]
    return jsonify({"message": "Tarefa deletada com sucesso!"}), 200



if __name__ == "__main__":
    app.run(debug=True)