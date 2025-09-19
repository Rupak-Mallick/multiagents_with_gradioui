from langchain_core.messages import convert_to_messages

def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    if not indent:
        return pretty_message
    indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
    return indented

def pretty_print_messages(update, last_message=False, return_string=False):
    output_text = ""
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        if len(ns) == 0:
            return ""
        graph_id = ns[-1].split(":")[0]
        output_text += f"Update from subgraph {graph_id}:\n\n"
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label
        output_text += update_label + "\n\n"

        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]

        for m in messages:
            output_text += pretty_print_message(m, indent=is_subgraph) + "\n"
        output_text += "\n"
    
    if return_string:
        return output_text
    else:
        print(output_text)