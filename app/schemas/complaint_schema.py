from typing import Optional

from pydantic import BaseModel, Field


class ComplaintExtraction(BaseModel):
    """
    Pydantic schema representing the exactly 13 required fields for a Pharmaceutical Complaint.
    """

    source: Optional[str] = Field(
        default=None,
        description="Complaint Source (e.g., Email, Phone, Document, Web Form)",
    )
    customerName: Optional[str] = Field(
        default=None,
        description="Customer Name or organization reporting the complaint",
    )
    productName: Optional[str] = Field(default=None, description="Product Name")
    productStrength: Optional[str] = Field(
        default=None, description="Product Strength or Grade (e.g., 500mg, USP)"
    )
    batchNumber: Optional[str] = Field(default=None, description="Batch or Lot Number")
    manufacturingDate: Optional[str] = Field(
        default=None, description="Manufacturing Date (YYYY-MM-DD)"
    )
    expiryDate: Optional[str] = Field(
        default=None, description="Expiry Date (YYYY-MM-DD)"
    )
    quantityAffected: Optional[str] = Field(
        default=None, description="Quantity Affected (e.g., 1000, 50kg)"
    )
    complaintType: Optional[str] = Field(
        default=None,
        description="Complaint Type (e.g., Packaging, Efficacy, Contamination, Adverse Event)",
    )
    complaintDate: Optional[str] = Field(
        default=None, description="Complaint Date (YYYY-MM-DD)"
    )
    complaintDescription: Optional[str] = Field(
        default=None, description="Detailed Complaint Description"
    )
    initialSeverity: Optional[str] = Field(
        default=None, description="Initial Severity (Critical, Major, Minor)"
    )
    priority: Optional[str] = Field(
        default=None, description="Priority (High, Medium, Low)"
    )
