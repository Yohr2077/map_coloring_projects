def select_unassigned_variable_mrv(variables, domains, assignment):
    """
    MRV = Minimum Remaining Value
    cchọn biến chưa gán có ít giá trị hợp lệ nhất.
    """
    unassigned = [v for v in variables if v not in assignment]

    #chọn biến có domain nhỏ nhất
    return min(unassigned, key=lambda var: len(domains[var]))


def degree_heuristic(var, graph, assignment):
    """
    Degree Heuristic:
    đếm số hàng xóm chưa gán màu của biến var
    """
    count = 0
    for neighbor in graph[var]:
        if neighbor not in assignment:
            count += 1
    return count


def select_unassigned_variable_mrv_degree(variables, domains, assignment, graph):
    """
    kết hợp MRV và Degree
    nếu nhiều biến cùng domain nhỏ nhất thì chọn biến có degree lớn nhất
    """
    unassigned = [v for v in variables if v not in assignment]

    #tìm domain nhỏ nhất
    min_size = min(len(domains[v]) for v in unassigned)

    candidates = [v for v in unassigned if len(domains[v]) == min_size]

    #nếu chỉ có 1 biến
    if len(candidates) == 1:
        return candidates[0]

    #chọn degree lớn nhất
    return max(candidates, key=lambda var: degree_heuristic(var, graph, assignment))


def order_domain_values_lcv(var, domains, graph, assignment):
    """
    LCv = Least Constraining Value
    sxep màu sao cho ít ảnh hưởng hàng xóm nhất
    """

    def count_conflicts(color):
        conflicts = 0
        for neighbor in graph[var]:
            if neighbor not in assignment:
                if color in domains[neighbor]:
                    conflicts += 1
        return conflicts

    return sorted(domains[var], key=count_conflicts)


def is_consistent(var, color, assignment, graph):
    """
    kiểm tra tô màu có hợp lệ k
    """
    for neighbor in graph[var]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True


def forward_check(var, color, domains, graph, assignment):
    """
    Forward Checking:sau khi gán màu cho var thì xóa màu đó khỏidomain hàng xóm
    """
    new_domains = {v: list(domains[v]) for v in domains}

    for neighbor in graph[var]:
        if neighbor not in assignment:
            if color in new_domains[neighbor]:
                new_domains[neighbor].remove(color)

            #nếu domain rỗng ->sai
            if len(new_domains[neighbor]) == 0:
                return None

    return new_domains
