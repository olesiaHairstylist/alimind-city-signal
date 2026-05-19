from app.core.status_view import (
    render_pipeline_status,
)


def main():
    view = render_pipeline_status()

    print(view)

    print("\nSTATUS_VIEW_V1 OK")


if __name__ == "__main__":
    main()