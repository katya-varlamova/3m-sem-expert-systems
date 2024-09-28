from items import Rule, Node, Label
from stack import Stack

class Search:
    def __init__(self, rule_arr: [Rule]):
        self.rule_arr = rule_arr

        self.goal_node = None
        self.solution_flg = 1
        self.no_solution_flg = 1

    def run(self, goal_node: Node, in_node_arr: [Node]):
        self.goal_node = goal_node
        self.set_nodes_closed(in_node_arr)

        while self.solution_flg and self.no_solution_flg:
            rule_cnt = self.parent_search()

            if self.solution_flg == 0:
                return

            if rule_cnt == 0:
                self.no_solution_flg = 0
                print("Solution was not found")


    def parent_search(self):
        cnt_rules = 0
        
        for rule in self.rule_arr:
            if self.solution_flg:
                if rule.label != Label.OPEN:
                    continue

                if self.is_close_nodes_cover(rule.node_arr):
                    print(f'Rule {rule.number}: all nodes are closed, added to opened')
                    rule.label = Label.CLOSE
                    self.set_nodes_closed(rule.node_arr)
                    rule.out_node.flag = Label.CLOSE

                    if rule.out_node == self.goal_node:
                        self.solution_flg = 0
                        print(f'Rule {rule.number} has output node equal to goal')
                        
                    cnt_rules += 1
            else:
                break
 

        print(f'Rule {rule.number} list of closed rules: ', end='')
        self.print_closed_rules()
        return cnt_rules

    def is_close_nodes_cover(self, in_node_arr: [Node]):
        for node in in_node_arr:
            if node.flag != Label.CLOSE:
                return False
        return True

    def set_nodes_closed(self, node_arr):
        for node in node_arr:
            node.flag = Label.CLOSE

    def print_closed_rules(self):
        for rule in self.rule_arr:
            if rule.label == Label.CLOSE:
                print(rule.number, end=' ')
        print()

    def print_nodes(self, node_arr: [Node]):
        for node in node_arr:
            print(node, end=' ')
        print()