from parsimonious import Grammar, NodeVisitor
import argparse
from pprint import pprint


# Define the grammar for the custom job script
grammar = Grammar(
    r"""
    job_script = (job / wait / ws)*

    job = "job" ws identifier ws parallel? ws "{" command "}" ws when?
    when = "when" ws "{" ws condition ws "}"
    wait = "wait"
    parallel = "PARALLEL"
    identifier = ~r"[a-zA-Z0-9_]+"
    command = ~r"[^{}]+"
    condition = ~r"[^{}]+"
    ws = ~r"\s*"
    """
)

# Define a visitor to process the parsed nodes
class JobVisitor(NodeVisitor):
    def visit_job(self, node, visited_children):
        _, _, name, _, parallel, _, _, command, _, _, *rest = visited_children
        return {
            "type": "job",
            "name": name,
            "parallel": parallel == [True],
            "command": command,
            "condition": rest[0][0] if isinstance(rest[0] , list) else None
        }

    def visit_wait(self, node, visited_children):
        return {
            "type": "wait",
        }

    def visit_parallel(self, node, visited_children):
        return True

    def visit_identifier(self, node, visited_children):
        return node.text

    def visit_command(self, node, visited_children):
        return node.text.strip()

    def visit_when(self, node, visited_children):
         return visited_children[4].text.strip()

    def generic_visit(self, node, visited_children):
        return visited_children or node

def main(job_file_path):
    with open(job_file_path, "r") as job_file:
        job_script = job_file.read()

    parsed_nodes = grammar.parse(job_script)
    visitor = JobVisitor()
    jobs = visitor.visit(parsed_nodes)

    pprint(jobs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run jobs from a custom job script")
    parser.add_argument("job_file", help="Path to the job script file")
    args = parser.parse_args()

    main(args.job_file)


