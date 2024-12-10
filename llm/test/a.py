from ollama import Client
import json 

client = Client(
  host='http://deepika:11435',
  headers={'x-some-header': 'some-value'}
)


# Simulates an API call to get flight times
# In a real application, this would fetch data from a live database or API
def get_flight_times(departure: str, arrival: str) -> str:
    print(f"I WAS CALLED {departure} {arrival}")
    flights = {
        'NYC-LAX': {'departure': '08:00 AM', 'arrival': '11:30 AM', 'duration': '5h 30m'},
        'LAX-NYC': {'departure': '02:00 PM', 'arrival': '10:30 PM', 'duration': '5h 30m'},
        'LHR-JFK': {'departure': '10:00 AM', 'arrival': '01:00 PM', 'duration': '8h 00m'},
        'JFK-LHR': {'departure': '09:00 PM', 'arrival': '09:00 AM', 'duration': '7h 00m'},
        'CDG-DXB': {'departure': '11:00 AM', 'arrival': '08:00 PM', 'duration': '6h 00m'},
        'DXB-CDG': {'departure': '03:00 AM', 'arrival': '07:30 AM', 'duration': '7h 30m'},
    }

    key = f'{departure}-{arrival}'.upper()
    return json.dumps(flights.get(key, {'error': 'Flight not found'}))


cache = []

def ask(q):
  cache.append( {
      'role': 'user',
      'content': q,
  })
  model = 'llama3.2'
  response = client.chat(model=model, messages=cache,  tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_flight_times",
                    "description": "Get the flight times between two cities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "departure": {
                                "type": "string",
                                "description": "The departure city (airport code)",
                            },
                            "arrival": {
                                "type": "string",
                                "description": "The arrival city (airport code)",
                            },
                        },
                        "required": ["departure", "arrival"],
                    },
                },
            }])  

  cache.append({
      'role': response.message.role, 
      'content': response.message.content, 
    })
  print(response.message.content)

  # Add the model's response to the conversation history
  cache.append(response["message"])

  # Check if the model decided to use the provided function

  if not response["message"].get("tool_calls"):
      print("The model didn't use the function. Its response was:")
      print(response["message"]["content"])
      return

  # Process function calls made by the model
  if response["message"].get("tool_calls"):
      available_functions = {
          "get_flight_times": get_flight_times,
         #  "search_data_in_vector_db": search_data_in_vector_db,
      }

      for tool in response["message"]["tool_calls"]:
          function_to_call = available_functions[tool["function"]["name"]]
          function_args = tool["function"]["arguments"]
          function_response = function_to_call(**function_args)

          # Add function response to the conversation
          cache.append(
              {
                  "role": "tool",
                  "content": function_response,
              }
          )

  # Second API call: Get final response from the model
  final_response = client.chat(model=model, messages=cache)

  print(final_response["message"]["content"])

while True:
  q = input(">>> ")
  ask(q)

