"""Human-edited script example.

Mục đích: minh họa file đã chỉnh sửa bởi nhóm sau khi nhận script từ AI.
"""

import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip().lower() for c in out.columns]
    out = out.drop_duplicates()
    return out


def main() -> None:
    input_path = "data/raw/example.csv"  # TODO: thay bằng path thật
    output_path = "data/processed/example_cleaned.csv"  # TODO: thay bằng path thật

    df = load_data(input_path)
    cleaned = basic_clean(df)
    cleaned.to_csv(output_path, index=False)

    print(f"Rows before: {len(df)}")
    print(f"Rows after : {len(cleaned)}")


if __name__ == "__main__":
    main()
