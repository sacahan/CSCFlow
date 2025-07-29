"""更新即時人流資料表結構

Revision ID: 20250729_003
Revises: 37bceec48d3d
Create Date: 2025-07-29 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20250729_003"
down_revision: Union[str, None] = "37bceec48d3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 移除舊索引
    op.drop_index("idx_real_time_flows_center_timestamp", table_name="real_time_flows")

    # 移除 center_id 欄位
    op.drop_column("real_time_flows", "center_id")

    # 新增 zip_code 欄位
    op.add_column(
        "real_time_flows", sa.Column("zip_code", sa.String(3), nullable=False)
    )

    # 新增索引
    op.create_index(
        "idx_real_time_flows_zip_timestamp",
        "real_time_flows",
        ["zip_code", "timestamp"],
    )


def downgrade() -> None:
    # 移除索引
    op.drop_index("idx_real_time_flows_zip_timestamp", table_name="real_time_flows")

    # 移除 zip_code 欄位
    op.drop_column("real_time_flows", "zip_code")

    # 新增 center_id 欄位
    op.add_column(
        "real_time_flows", sa.Column("center_id", postgresql.UUID(), nullable=False)
    )

    # 新增索引
    op.create_index(
        "idx_real_time_flows_center_timestamp",
        "real_time_flows",
        ["center_id", "timestamp"],
    )
