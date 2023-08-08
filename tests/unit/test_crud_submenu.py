import pytest

from .config_test.config_submenu import BaseTestSubmenu


@pytest.mark.order(2)
@pytest.mark.asyncio
class TestCRUDSubmenu:
    base = BaseTestSubmenu()

    async def test_create_menu(self) -> None:
        response = await self.base.menu_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_menu

    async def test_get_empty_list_submenu(self) -> None:
        response = await self.base.submenu_test_get_list()
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_submenu(self) -> None:
        response = await self.base.submenu_test_create()
        assert response.status_code == 201
        assert response.json() == self.base.check_data_submenu

    async def test_get_submenu(self) -> None:
        response = await self.base.submenu_test_get()
        assert response.status_code == 200
        assert response.json() == self.base.check_data_submenu

    async def test_update_submenu(self) -> None:
        response = await self.base.submenu_test_update()
        assert response.status_code == 200
        assert response.json() == self.base.update_check_data_submenu

    async def test_delete_submenu(self) -> None:
        response = await self.base.submenu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_submenu

    async def test_not_found_submenu(self) -> None:
        response = await self.base.submenu_test_get()
        assert response.status_code == 404
        assert response.json() == self.base.not_found_submenu

    async def test_delete_menu(self) -> None:
        response = await self.base.menu_test_delete()
        assert response.status_code == 200
        assert response.json() == self.base.successful_delete_menu
