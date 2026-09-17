"""
Entry point: a simple chat loop where you type commands and the agent
generates / uploads videos accordingly.

Commands:
  generate video: "<topic>"              -> writes script + renders video
  generate script: "<full script text>"  -> uses YOUR exact script (no AI rewrite)
  upload last video                      -> uploads with 'private' visibility
  publish last video                     -> uploads with 'public' visibility
  generate and upload: "<topic>"         -> does both, private by default
  set title: <text>
  set description: <text>
  help
  exit
"""
from agent import Agent

HELP_TEXT = __doc__


def parse_and_run(agent: Agent, line: str):
    lower = line.strip().lower()

    if lower in ("exit", "quit"):
        return False

    if lower in ("help", "?"):
        print(HELP_TEXT)
        return True

    if lower.startswith("generate and upload:"):
        topic = line.split(":", 1)[1].strip().strip('"')
        agent.generate_and_upload(topic)
        return True

    if lower.startswith("generate script:"):
        script = line.split(":", 1)[1].strip().strip('"')
        agent.generate(script, is_full_script=True)
        return True

    if lower.startswith("generate video:"):
        topic = line.split(":", 1)[1].strip().strip('"')
        agent.generate(topic)
        return True

    if lower.startswith("upload last video"):
        agent.upload(privacy_status="private")
        return True

    if lower.startswith("publish last video"):
        agent.upload(privacy_status="public")
        return True

    if lower.startswith("set title:"):
        agent.set_title(line.split(":", 1)[1].strip())
        return True

    if lower.startswith("set description:"):
        agent.set_description(line.split(":", 1)[1].strip())
        return True

    print(
        "Command not recognized. Type 'help' to see available commands."
    )
    return True


def main():
    print("🎬 YouTube AI Agent — type 'help' for commands, 'exit' to quit.\n")
    agent = Agent()
    running = True
    while running:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        running = parse_and_run(agent, line)


if __name__ == "__main__":
    main()
