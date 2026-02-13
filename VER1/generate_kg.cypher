LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/lavishlyinspired/GraphDBExperiments/refs/heads/main/VER1/Lungcancerinfo.csv' AS row
CREATE (a:Article { uri: row.uri})
SET a.title = row.title, a.body = row.body, a.datetime = datetime(row.date);