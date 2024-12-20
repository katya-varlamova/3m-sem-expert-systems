from items import *
from stack import Stack
import copy

class Search:
    def __init__(self, rule_arr: [Rule]):
        self.rule_arr = rule_arr  # база знаний
        self.open_node_st = Stack()
        self.open_rule_lst = []
        self.close_node_lst = []
        self.close_rule_lst = []
        self.prohibited_node_lst = []
        self.prohibited_rule_lst = []
        self.tables = Stack()

        self.goal_node = None
        self.solution_flg = 1
        self.no_solution_flg = 1
        self.no_label = 1
        self.table = Table()

    def run(self, goal_node: Node, in_node_arr: [Node]):
        self.goal_node = goal_node
        self.open_node_st.push(goal_node)
        self.tables.push(copy.deepcopy(self.table))
        self.close_node_lst = in_node_arr

        while self.solution_flg and self.no_solution_flg:
            rule_cnt = self.child_search()

            # solution was found
            if self.solution_flg == 0:
                print("Solution was found")
                return

            if rule_cnt == 0 and self.open_node_st.length() < 2:
                self.no_solution_flg = 0
                print("Solution was not found")
            elif rule_cnt == 0:
                print("Backtracking process is going to be launched")
                self.backtracking()

    def child_search(self):
        cnt_rules = 0

        for rule in self.rule_arr:
            print(f'[Rule {rule.number}] Current rule {rule}')

            current_node = self.open_node_st.peek()
            print(f'[Node {current_node}]  Current node')

            if rule.label != Label.OPEN: # посещённые
                print(f'[Rule {rule.number}] was already processed')
                print('-' * 128 + '\n')
                continue

            if unification(self.table, rule.out_node, current_node):
                print(f'[Rule {rule.number}] has out node that equals goal one')

                rule.label = Label.VIEWED
                self.open_rule_lst.append(rule)
                is_new_goal_added = self.add_new_goal(rule.node_arr)
                if not is_new_goal_added:
                    print("Label process is going to be launched")
                    self.label()

                cnt_rules += 1
                self.print_info(rule)
                break

            if self.is_prohibited_node_exist(rule.node_arr):
                self.prohibited_rule_lst.append(rule)
                rule.label = Label.FORBIDDEN

                self.print_info(rule)
                continue

            #self.print_info(rule)

        return cnt_rules

    def get_fact(self, node, table):
        new_terms = []
        for term in node.terminals:
            if term.variable:
                if type(table.variables[term.name]) is str:
                    print("Error")
                else:
                    new_terms.append(table.variables[term.name])
            else:
                new_terms.append(term)
        return Node(node.name, new_terms)

    def label(self):
        while True:
            rule = self.open_rule_lst.pop()
            self.close_rule_lst.append(rule)

            node = self.open_node_st.pop()
            self.tables.pop()
            fact = self.get_fact(node, self.table)
            self.close_node_lst.append(fact)

            print(f'[Labelling] Rule {rule} was added to close rules')
            print(f'[Labelling] Node {fact} was added to close nodes')

            if unification(self.table, fact, self.goal_node):
                self.solution_flg = 0
                return

            current_node = self.open_node_st.peek()
            current_rule = self.open_rule_lst[-1]
            if not unification(self.table, current_rule.out_node, current_node):
                return

    def backtracking(self):
        current_goal = self.open_node_st.pop()

        table_prev = self.tables.pop()
        self.table = self.tables.peek()
        rule = self.open_rule_lst.pop()

        current_goal.flag = Label.FORBIDDEN
        self.prohibited_node_lst.append(current_goal)

        rule.label = Label.FORBIDDEN
        self.prohibited_rule_lst.append(rule)
        self.print_info(rule)
        print(f'[Backtrack] Rule {rule} was added to prohibited rules')
        print(f'[Backtrack] Node {current_goal} was added to prohibited nodes')
        print(f'[Backtrack] Table {table_prev.variables} was changed to {self.table.variables}')

        for node in rule.node_arr:
            print(f'[Backtrack] Node {node} should be removed from opened nodes')
            self.open_node_st.remove_element(node)
        print()

    def add_new_goal(self, node_arr: [Node]):
        new_goal_flg = False
        for node in node_arr[::-1]:
            found = False
            for node_closed in self.close_node_lst:
                if unification(self.table, node, node_closed):
                    found = True
            if not found:    
                self.open_node_st.push(node)
                copy_table = copy.deepcopy(self.table)
                self.tables.push(copy_table)
                new_goal_flg = True
        return new_goal_flg

    def is_prohibited_node_exist(self, node_arr: [Node]):
        for node in node_arr:
            if node in self.prohibited_node_lst:
                return True
        return False

    def print_nodes(self, node_arr: [Node]):
        for node in node_arr:
            print(node, end=' ')
        print()

    def print_rules(self, rule_arr: [Rule]):
        for rule in rule_arr:
            print(rule.number, end=' ')
        print()

    def print_info(self, rule: Rule):
        print(f'[Rule {rule.number}] list of opened nodes: ', end='    ')
        self.open_node_st.show()
        print(f'[Rule {rule.number}] list of closed nodes: ', end='    ')
        self.print_nodes(self.close_node_lst)
        print(f'[Rule {rule.number}] list of prohibited nodes: ', end='')
        self.print_nodes(self.prohibited_node_lst)
        print(f'[Rule {rule.number}] list of opened rules: ', end='    ')
        self.print_rules(self.open_rule_lst)
        print(f'[Rule {rule.number}] list of closed rules: ', end='    ')
        self.print_rules(self.close_rule_lst)
        print(f'[Rule {rule.number}] list of prohibited rules: ', end='')
        self.print_rules(self.prohibited_rule_lst)

        print('-' * 128 + '\n')
        print(f"Current table: {self.table.variables}")
