FROM ubuntu

CMD ["sh", "-c", "while true; do echo $TAVILY_API_KEY $OPENAI_API_KEY; sleep 10; done"]
