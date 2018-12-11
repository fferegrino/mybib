def entry_to_node(entry):
    copied = entry.copy()
    return_value = f'CREATE (:Paper {{'
    return_value += ', '.join([f'{k}:"{copied[k]}"' for k in copied]) + '})'
    return return_value


def link_papers(referee_key, referenced_key, number, comment):
    return_value = f'MATCH (citer:Paper{{ID:"{referee_key}"}}),(cited:Paper{{ID:"{referenced_key}"}}) ' \
                   f'CREATE (citer)-[r:CITED{{number:{number}, comment:{comment} }}]->(cited) RETURN r'
    return return_value
