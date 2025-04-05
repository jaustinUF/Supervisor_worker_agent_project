def prnt_msg(messages):
    """Print the message trace from LangGraph agents"""
    print("\n🧠 Agent Message Trace:")
    print("=" * 60)

    for i, msg in enumerate(messages):
        msg_type = msg.__class__.__name__
        print(f"\nStep {i + 1}: {msg_type}")
        print("-" * 60)

        if msg_type == "HumanMessage":
            print(f"🗣️ User: {msg.content}")
        elif msg_type == "AIMessage":
            content = msg.content.strip()
            print(f"🤖 Agent reply: {content if content else '[no direct reply]'}")

            # If tool calls are embedded
            if "tool_calls" in msg.additional_kwargs:
                for call in msg.additional_kwargs["tool_calls"]:
                    fn = call["function"]["name"]
                    args = call["function"]["arguments"]
                    print(f"🔧 Tool call → {fn}({args})")
        elif msg_type == "ToolMessage":
            print(f"🔧 Tool '{msg.name}' responded:\n{msg.content}")
        else:
            print(f"(Unhandled message type: {msg_type})")
    print("=" * 60 + "\n")
