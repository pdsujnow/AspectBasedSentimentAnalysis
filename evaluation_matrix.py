import config, re


def precision(extracted_aspect_list):
    """
    Calculate precision
    :param extracted_aspect:
    :param actual_aspect:
    :return:
    """
    # precision = extracted_aspect intersection actual_aspect/extracted_aspect
    actual_aspect = get_actual_aspect()
    extracted_aspect = []
    for aspect, count in extracted_aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        extracted_aspect.append(aspect_replacing_space_with_underscore)

    print(len(extracted_aspect),extracted_aspect)
    print(len(actual_aspect),actual_aspect)

    ext_asp_intersection_actual = []
    for ex_asp in extracted_aspect:
        if ex_asp in actual_aspect:
            ext_asp_intersection_actual.append(ex_asp)
    print(len(ext_asp_intersection_actual),ext_asp_intersection_actual)
    precision_value = len(ext_asp_intersection_actual) / len(extracted_aspect)
    print(precision_value)
    # return precision_value


def recall(extracted_aspect_list):
    """
    Calculate recall
    :param extracted_aspect:
    :param actual_aspect:
    :return:
    """
    # recall = extracted_aspect intersection actual_aspect/actual_aspect
    actual_aspect = get_actual_aspect()
    extracted_aspect = []
    for aspect, count in extracted_aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        extracted_aspect.append(aspect_replacing_space_with_underscore)

    print(len(extracted_aspect), extracted_aspect)
    print(len(actual_aspect), actual_aspect)

    ext_asp_intersection_actual = []
    for ex_asp in extracted_aspect:
        if ex_asp not in actual_aspect:
            ext_asp_intersection_actual.append(ex_asp)
    print(len(ext_asp_intersection_actual), ext_asp_intersection_actual)
    recall_value = len(ext_asp_intersection_actual) / len(actual_aspect)
    print(recall_value)
    return recall_value


def f_measure(precision, recall):
    """
    Calculate f-measure
    :param precision:
    :param recall:
    :return:
    """
    # f-measure = 2 *  precision * recall / precision + recall
    f_measure_value = (2 * precision * recall) / (precision + recall)
    return f_measure_value


def get_actual_aspect():
    file = open(config.Output_file_path + "my_product_aspects_list_router.txt", "r").read()
    actual_product = file.split('\n')
    return actual_product
