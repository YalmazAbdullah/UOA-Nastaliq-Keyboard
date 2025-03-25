import pandas as pd
from graphviz import Digraph

# Sample DataFrame
data = pd.read_csv('./DiscountEvaluation/data/dyad/combined_dataset.csv')

binary_variables = ['SameHand', 'SameFinger', 'SameKey', 'Reach', 'Hurdle']

total_frequency = data["Frequency"].sum()

print("Total Frequency:", total_frequency)

def create_tree(df, variables, graph, parent_name="root", leaf_nodes=None):
    if leaf_nodes is None:
        leaf_nodes = []

    if not variables:
        count = df['Frequency'].sum() / total_frequency
        rounded = round(count, -int(f"{count:.1e}".split('e')[1]) + 2)
        if count > 0:
            node_name = f"{parent_name}_leaf"
            graph.node(node_name, label=f"{rounded}", shape="box", width="0.5", height="0.5")
            graph.edge(parent_name, node_name, penwidth="1.5")
            leaf_nodes.append(node_name)  # Track leaf nodes
            return True
        return False

    current_var = variables[0]

    # Apply rules
    if current_var == "Hurdle":
        # If "Reach" is False, skip branching for "Hurdle"
        if "Reach_false" in parent_name:
            return create_tree(df, variables[1:], graph, parent_name)

        # If "SameKey=True" and "SameFinger=True", set "Hurdle=False" directly
        if "SameKey_true" in parent_name and "SameFinger_true" in parent_name:
            filtered_df = df[df["Hurdle"] == 0]
            return create_tree(filtered_df, variables[1:], graph, parent_name)

    if current_var == "SameFinger":
        # If "SameHand" is False or "SameKey" is False, skip branching for "SameFinger"
        if "SameHand_false" in parent_name or "SameKey_false" in parent_name:
            return create_tree(df, variables[1:], graph, parent_name)

    if current_var == "SameKey":
        # If "SameHand" is False, skip branching for "SameKey"
        if "SameHand_false" in parent_name:
            return create_tree(df, variables[1:], graph, parent_name)

    true_df = df[df[current_var] == 1]
    false_df = df[df[current_var] == 0]

    # Process True Branch
    true_branch_valid = False
    if not true_df.empty:
        true_name = f"{parent_name}_{current_var}_true"
        graph.node(true_name, label=f"{current_var} = True",shape = "box", width="0.8", height="0.5")
        graph.edge(parent_name, true_name, penwidth="1.5")
        true_branch_valid = create_tree(true_df, variables[1:], graph, true_name)

    # Process False Branch
    false_branch_valid = False
    if not false_df.empty:
        false_name = f"{parent_name}_{current_var}_false"
        graph.node(false_name, label=f"{current_var} = False", shape = "box", width="0.8", height="0.5")
        graph.edge(parent_name, false_name, penwidth="1.5")
        false_branch_valid = create_tree(false_df, variables[1:], graph, false_name)

    return true_branch_valid or false_branch_valid

# Align Leaves Vertically
def align_leaves(graph, leaf_nodes):
    with graph.subgraph() as sub:
        sub.attr(rank="same")
        for leaf in leaf_nodes:
            sub.node(leaf)

# Generate separate trees for each Keyboard category
keyboard_categories = data['Keyboard'].unique()

for keyboard in keyboard_categories:
    subset = data[data['Keyboard'] == keyboard]
    dot = Digraph(comment=f"Binary Variables Tree ({keyboard})")
    
    # Adjust layout for compactness
    dot.attr(dpi="300", size="6,6")  # Adjust DPI and graph size
    dot.attr('graph', nodesep="0.2", ranksep="0.3")  # Reduce spacing between nodes and ranks
    dot.attr('node', fontsize="24")  # Reduce font size for nodes
    dot.node("root", "Start")

    # Create tree for the subset of data
    leaf_nodes = []
    has_valid_leaves = create_tree(subset, binary_variables, dot, leaf_nodes=leaf_nodes)

    if has_valid_leaves:
        align_leaves(dot, leaf_nodes)

    # Render and save the tree diagram
    if has_valid_leaves:
        output_file = f"binary_tree_{keyboard}_compact"
        dot.render(output_file, format="svg", cleanup=True)
        print(f"Compact tree saved for Keyboard: {keyboard} as {output_file}.png")
    else:
        print(f"No valid branches or leaves for Keyboard: {keyboard}.")