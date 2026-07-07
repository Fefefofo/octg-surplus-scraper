"""Pydantic data models for surplus OCTG pipe listings."""

from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl


class OCTGListing(BaseModel):
    company_name: str | None = Field(default=None, description="Seller or broker company name.")
    pipe_grade: str | None = Field(default=None, description="OCTG grade, for example J55, N80, L80, P110.")
    diameter: str | None = Field(default=None, description="Outside diameter, usually in inches.")
    wall_thickness: str | None = Field(default=None, description="Wall thickness or weight per foot.")
    length: str | None = Field(default=None, description="Pipe length, range, or random length note.")
    quantity: str | None = Field(default=None, description="Available quantity, joints, feet, or tons.")
    price: str | None = Field(default=None, description="Published price, quote note, or bid status.")
    location: str | None = Field(default=None, description="Yard, city/state, region, or country.")
    contact_email: str | None = Field(default=None, description="Public contact email if listed.")
    source_url: HttpUrl | str = Field(description="URL where the listing was found.")
