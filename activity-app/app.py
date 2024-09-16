import uuid

from flask import Flask, request, jsonify
import traceback  # Import traceback for detailed error messages

from rag import rag

import db

app = Flask(__name__) 

@app.route("/question", methods=["POST"])
def handle_question():
    try:
        print("Received a POST request at /question")

        data = request.json
        if data is None:
            print("No JSON data in the request")
            return jsonify({"error": "No JSON data provided"}), 400

        question = data.get("question")
        if not question:
            return jsonify({"error": "No question provided"}), 400

        conversation_id = str(uuid.uuid4())
        print(f"Received question: {question}")
        
        # Call your RAG function and print detailed output
        answer_data = rag(question)
        print(f"Answer generated: {answer_data}")

        result = {
            "conversation_id": conversation_id,
            "question": question,
            "answer": answer_data["answer"],
        }

        print(f"Saving conversation: {conversation_id}")
        db.save_conversation(
            conversation_id=conversation_id,
            question=question,
            answer_data=answer_data,
        )

        return jsonify(result)
    
    except Exception as e:
        # Capture full traceback for debugging
        error_message = ''.join(traceback.format_exc())
        print(f"Error occurred: {error_message}")  # Print the full stack trace
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@app.route("/feedback", methods=["POST"])
def handle_feedback():
    data = request.json
    conversation_id = data["conversation_id"]
    feedback = data["feedback"]

    if not conversation_id or feedback not in [1, -1]:
        return jsonify({"error": "Invalid input"}), 400

    db.save_feedback(
        conversation_id=conversation_id,
        feedback=feedback,
    )

    result = {
        "message": f"Feedback received for conversation {conversation_id}: {feedback}"
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)