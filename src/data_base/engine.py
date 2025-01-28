from sqlalchemy import create_engine


class DatabaseEngine:
    """Улучшенный класс для управления движком базы данных."""

    def __init__(self, url: str, echo: bool = False):
        self.url = url
        self.echo = echo
        try:
            self.engine = self._create_engine()
        except Exception as ex:
            # logging.error(f"Ошибка при инициализации движка: {ex}", exc_info=True)
            raise RuntimeError("Инициализация движка базы данных не удалась.") from ex

    def _create_engine(self):
        """Вспомогательный метод для создания движка."""
        return create_engine(self.url, echo=self.echo)

    def test_connection(self) -> None:
        """Проверяет доступность базы данных."""
        try:
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
        except Exception as ex:
            raise RuntimeError("База данных недоступна.") from ex

    def restart_engine(self, url: str = None, echo: bool = None) -> None:
        """Перезапускает движок с новыми параметрами."""
        self.engine.dispose()
        self.url = url or self.url
        self.echo = echo if echo is not None else self.echo
        self.engine = self._create_engine()

    def get_engine(self, ensure_available: bool = False):
        """Возвращает движок, проверяя доступность при необходимости."""
        if ensure_available:
            self.test_connection()
        return self.engine