use PROJECT_PC01

CREATE TABLE conteo(
idconteo int identity primary key,
fecha date,
entradas int
);

insert into conteo values('2023-04-28', 1)

select * from conteo


-----PRUEBA
CREATE TABLE sumConteo(
idsumConteo int identity primary key,
idconteo int foreign key references conteo(idconteo),
fechaConteo varchar(50),
sumConteo int
);

CREATE PROCEDURE Día
as
SELECT fecha
FROM conteo
WHERE fecha = fecha
group by fecha
order by fecha DESC
go

CREATE PROCEDURE ConteoMesDesc
AS
SELECT DATENAME(MONTH, DATEADD(MONTH,MONTH(fecha)- 1, '1900-01-01')) Mes, SUM(entradas) AS 'Total Personas'
FROM conteo
WHERE MONTH(fecha) =  MONTH(fecha)
group by MONTH(fecha)
order by MONTH(fecha) DESC
go

SELECT YEAR(fecha) Año, SUM(entradas) As 'Total Personas'
FROM conteo
WHERE YEAR(fecha) = YEAR(fecha)
group by YEAR(fecha)
 
 exec Día
 exec ConteoMesDesc

