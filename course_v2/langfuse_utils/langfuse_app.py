from langfuse import Langfuse 

class LangfuseApp:
    def __init__(self):
        self.langfuse = Langfuse()

    def add_langfuse_score(self, trace_id, score, comment):
        try:
            self.langfuse.score(
                trace_id=trace_id, 
                name="accuracy",
                value=score, 
                data_type="NUMERIC",
                comment=comment 
            )
            return "Success"
        except Exception as e:
            print("Error logging score into Langfuse")
            print(e)
            return "Error"
