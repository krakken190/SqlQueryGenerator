from flask import Flask, render_template, request, session
import openai

app = Flask(__name__)
app.secret_key = ""   # give any name to your secret key

openai.api_key = ""#add your open ai api key here

def generate_sql(schema, prompt):
    # This function will take the schema and user prompt, process them, and call the OpenAI API to generate the SQL query
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Given the following MySQL schema:\n{schema}\nWrite a SQL query to answer the prompt: {prompt}",
        max_tokens=150,  
        n=1,
        stop=None,
        temperature=0.7,  
    )
    return response.choices[0].text.strip()

@app.route('/')
def home():
    session.pop("sql_query", None)
    return render_template('home.html')

@app.route('/generate_query', methods=['POST'])
def generate_query():
    schema = request.form['schema']
    prompt = request.form['prompt']
    
    sql_query = generate_sql(schema, prompt)
    return render_template('result.html', sql_query=sql_query)

@app.route('/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run(debug=True)
