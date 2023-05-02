use PROJECT_PC01

CREATE TABLE conteo(
idconteo int identity primary key,
fecha varchar(50),
entradas int
);


insert into conteo values('2/5/2023', 1)

select * from conteo


-----PRUEBA
CREATE TABLE sumConteo(
idsumConteo int identity primary key,
idconteo int foreign key references conteo(idconteo),
fechaConteo varchar(50),
sumConteo int
);