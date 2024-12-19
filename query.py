from SPARQLWrapper import SPARQLWrapper, JSON

# Define the SPARQL endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# Define the SPARQL query
query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?team
WHERE {
  # Teams for Mark Messier
  dbr:Mark_Messier dbo:formerTeam ?team .
  # Teams for Wayne Gretzky
  dbr:Wayne_Gretzky dbo:formerTeam ?team .
}
"""

# Set up the SPARQL query
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# Execute the query and process results
try:
    results = sparql.query().convert()
    print("These are the teams that both players played for")
    print("-" * 40)

    # Parse and print the results
    for result in results["results"]["bindings"]:
        team = result["team"]["value"].split("/")[-1]
        
        print(f"Team: {team}")
        print("-" * 40)
except Exception as e:
    print(f"An error occurred: {e}")
