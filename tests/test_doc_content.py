class TestDocContent:
    """These tests have been added to check the resolution of
    CartoCSS documentation errors reported to Carto developer team.
    More information at https://github.com/mondeja/cartocss-doc-parser/issues/1

    If one of the next test fails, means that errors in CartoCSS documentation
    has been solved and the source code of this library must be updated.
    """

    def test_opacity_common_elements_section(self, soup):
        section_table = soup.find(id="common-elements").find_next()
        while section_table.name != "table":
            section_table = section_table.find_next()
        link = section_table.find_all("td")[2].find("a")
        assert link.text == "opacity float"

    def test_point_comp_op_point_section(self, soup):
        point_comp_op_keyword_h = soup.find(id="point-comp-op-keyword")
        assert point_comp_op_keyword_h.text == "point-comp-op `keyword"

    def test_torque_aggregation_function_link(self, soup):
        table = soup.find(id="torque-cartocss-properties").find_next()
        link = table.find_all("td")[3].find("a")
        assert link.attrs["href"] == "{#-torque-aggregation-function-keyword"

    def test_torque_aggregation_function_table_available_values(self, soup):
        table = soup.find(
            id="-torque-aggregation-function-keyword",
        ).find_next()
        while table.name != "table":
            table = table.find_next()
        td = table.find_all("tr")[3].find_all("td")[1]
        assert len(td.find_all("code")) == 1
