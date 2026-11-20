from pydantic import BaseModel, ConfigDict, Field


class EditorialBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    pais: str = Field(min_length=1, max_length=80)
    email: str = Field(min_length=3, max_length=150)


class EditorialCreate(EditorialBase):
    pass


class EditorialOut(EditorialBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class LibroBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    autor: str = Field(min_length=1, max_length=150)
    isbn: str = Field(min_length=10, max_length=20)
    anio: int = Field(ge=1000, le=2100)
    existencia: int = Field(ge=0)
    editorial_id: int


class LibroCreate(LibroBase):
    pass


class LibroOut(LibroBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UsuarioCreate(BaseModel):
    nomuser: str = Field(min_length=3, max_length=50)
    passwd: str = Field(min_length=6, max_length=100)
    nombrecompleto: str = Field(min_length=1, max_length=150)


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nomuser: str
    nombrecompleto: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
