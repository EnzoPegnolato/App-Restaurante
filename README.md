Programa Usados --- MySQL Workbench 8.0 CE ------ Wampserver64--------- Pycharm

Script do MySQL:
OBS: Alguns Dados já foram inseridos para facilitar o uso.

create database restaurante;
 
create table cadastros(

id int not null primary key auto_increment,
nome varchar(50) not null,
senha varchar(20) not null,
nivel int not null
 
 
);
 
insert into cadastros(nome, senha, nivel) values ('admin', 'admin', 2);
 

 
create table produtos(
id int auto_increment not null primary key,
nome varchar(100) not null,
ingredientes varchar(1000),
grupo varchar(100),
preco float
 
);
 

 
create table pedidos(
id int not null primary key auto_increment,
nome varchar(100) not null,
ingredientes varchar(1000),
grupo varchar(100),
localEntrega varchar(500),
observacoes varchar(1000)
 
);
 
select * from produtos;
 
insert into pedidos (nome, ingredientes, grupo, localEntrega, observacoes) values ('pizza de mussarela', 'mussarela', 'pizzas', '', 'sem cebola');
insert into pedidos (nome, ingredientes, grupo, localEntrega, observacoes) values ('coca', '', 'bebidas', '', '');
 

 
create table estatisticaVendido(
 
id int not null primary key auto_increment,
nome varchar(100) not null,
grupo varchar(100),
preco float
	
 
);
 
insert into estatisticaVendido(nome, grupo, preco) values ('pizza de mussarela', 'pizzas', 34.90);
 
insert into estatisticaVendido(nome, grupo, preco) values ('coca', 'bebidas', 6);
 
insert into estatisticaVendido(nome, grupo, preco) values ('pizza de portuguesa', 'pizzas', 34.90);
 
insert into estatisticaVendido(nome, grupo, preco) values ('suco de laranja', 'pizzas', 7);


