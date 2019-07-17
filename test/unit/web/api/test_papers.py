from copy import deepcopy
from unittest.mock import Mock, patch

from mybib.graphql.access_layer import EntityAlreadyExistsError

validate_indexes = Mock()


@patch("mybib.web.api.papers.insert_paper", autospec=True)
def test_post_inserts(
    insert_paper_mock,
    authenticated_post,
    bibtex_multiple_authors,
    single_doc_multiple_authors,
):
    insert_paper_mock.return_value = single_doc_multiple_authors

    inserted_paper = deepcopy(single_doc_multiple_authors)
    inserted_paper["_bibtex"] = bibtex_multiple_authors

    response = authenticated_post("/api/papers", data=bibtex_multiple_authors)

    insert_paper_mock.assert_called_once_with(inserted_paper)
    assert response.status_code == 201


@patch("mybib.web.api.papers.insert_paper", autospec=True)
def test_post_inserts_already_exist(
    insert_paper_mock,
    authenticated_post,
    bibtex_multiple_authors,
    single_doc_multiple_authors,
):
    insert_paper_mock.side_effect = EntityAlreadyExistsError()
    inserted_paper = deepcopy(single_doc_multiple_authors)
    inserted_paper["_bibtex"] = bibtex_multiple_authors

    response = authenticated_post("/api/papers", data=bibtex_multiple_authors)

    insert_paper_mock.assert_called_once_with(inserted_paper)
    assert response.status_code == 409
