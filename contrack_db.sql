--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

-- Started on 2024-06-27 23:10:02

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3388 (class 1262 OID 49180)
-- Name: contrack_db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE contrack_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Philippines.1252';


ALTER DATABASE contrack_db OWNER TO postgres;

\connect contrack_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 57417)
-- Name: contracts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contracts (
    ac_id integer NOT NULL,
    ac_ups_title character varying(100) NOT NULL,
    ac_ups_type character varying(50) NOT NULL,
    ac_ups_desc character varying(500) NOT NULL,
    ac_ups_ipname character varying(100) NOT NULL,
    ac_tin timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ac_ups_sc1 character varying(50) NOT NULL,
    ac_ups_sched1done boolean DEFAULT false NOT NULL,
    ac_ip_loi bytea,
    ac_ups_aloi boolean DEFAULT false,
    ac_ups_con bytea,
    ac_ip_fb1 character varying(1000) DEFAULT NULL::character varying,
    ac_ip_fbd1 boolean DEFAULT false,
    ac_ip_fb2 character varying(1000) DEFAULT NULL::character varying,
    ac_ip_fbd2 boolean DEFAULT false,
    ac_ip_fb3 character varying(1000) DEFAULT NULL::character varying,
    ac_ip_fbd3 boolean DEFAULT false,
    ac_ip_doc1 bytea,
    ac_ip_docd1 boolean DEFAULT false,
    ac_ip_doc2 bytea,
    ac_ip_docd2 boolean DEFAULT false,
    ac_ip_doc3 bytea,
    ac_ip_docd3 boolean DEFAULT false,
    ac_ups_fb1 character varying(1000) DEFAULT NULL::character varying,
    ac_ups_fbd1 boolean DEFAULT false,
    ac_ups_fb2 character varying(1000) DEFAULT NULL::character varying,
    ac_ups_fbd2 boolean DEFAULT false,
    ac_ups_fb3 character varying(1000) DEFAULT NULL::character varying,
    ac_ups_fbd3 boolean DEFAULT false,
    ac_ups_doc1 bytea,
    ac_ups_docd1 boolean DEFAULT false,
    ac_ups_doc2 bytea,
    ac_ups_docd2 boolean DEFAULT false,
    ac_ups_doc3 bytea,
    ac_ups_docd3 boolean DEFAULT false,
    ac_ip_final character varying(50) DEFAULT NULL::character varying,
    ac_ups_final character varying(50) DEFAULT NULL::character varying,
    ac_ups_meet character varying(50) DEFAULT NULL::character varying,
    ac_ups_meetd boolean DEFAULT false,
    ac_ovpla_sign character varying(50) DEFAULT NULL::character varying,
    ac_ovpla_docfin bytea,
    ac_ovpla_docfind character varying(50) DEFAULT NULL::character varying,
    ac_tout timestamp without time zone,
    ac_percent character varying(10) NOT NULL,
    ac_delete boolean
);


ALTER TABLE public.contracts OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 57416)
-- Name: contracts_ac_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contracts_ac_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contracts_ac_id_seq OWNER TO postgres;

--
-- TOC entry 3389 (class 0 OID 0)
-- Dependencies: 214
-- Name: contracts_ac_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contracts_ac_id_seq OWNED BY public.contracts.ac_id;


--
-- TOC entry 219 (class 1259 OID 57475)
-- Name: indpartners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.indpartners (
    ip_id integer NOT NULL,
    ip_name character varying(50) NOT NULL,
    ip_ind character varying(30) NOT NULL,
    ip_person character varying(50) NOT NULL,
    ip_phone character varying(20),
    ip_email character varying(50),
    ip_add timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ip_upd timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ip_remarks character varying(500) NOT NULL,
    ip_delete boolean DEFAULT false NOT NULL
);


ALTER TABLE public.indpartners OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 57474)
-- Name: indpartners_ip_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.indpartners_ip_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.indpartners_ip_id_seq OWNER TO postgres;

--
-- TOC entry 3390 (class 0 OID 0)
-- Dependencies: 218
-- Name: indpartners_ip_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.indpartners_ip_id_seq OWNED BY public.indpartners.ip_id;


--
-- TOC entry 217 (class 1259 OID 57453)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_fname character varying(50) NOT NULL,
    user_lname character varying(50) NOT NULL,
    user_email character varying(50) NOT NULL,
    user_cname character varying(100) NOT NULL,
    user_pwd character varying(500) NOT NULL,
    user_access character varying(20) NOT NULL,
    user_crt timestamp without time zone DEFAULT now() NOT NULL,
    user_lastupd timestamp without time zone DEFAULT now() NOT NULL,
    user_delete boolean DEFAULT false,
    user_r1 boolean DEFAULT false,
    user_r2 boolean DEFAULT false,
    user_r3 boolean DEFAULT false,
    user_r4 boolean DEFAULT false,
    user_r5 boolean DEFAULT false,
    user_r6 boolean DEFAULT false,
    user_r7 boolean DEFAULT false,
    user_r8 boolean DEFAULT false,
    user_r9 boolean DEFAULT false,
    user_r10 boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 57452)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 3391 (class 0 OID 0)
-- Dependencies: 216
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 3183 (class 2604 OID 57420)
-- Name: contracts ac_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contracts ALTER COLUMN ac_id SET DEFAULT nextval('public.contracts_ac_id_seq'::regclass);


--
-- TOC entry 3225 (class 2604 OID 57478)
-- Name: indpartners ip_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.indpartners ALTER COLUMN ip_id SET DEFAULT nextval('public.indpartners_ip_id_seq'::regclass);


--
-- TOC entry 3211 (class 2604 OID 57456)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 3378 (class 0 OID 57417)
-- Dependencies: 215
-- Data for Name: contracts; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.contracts (ac_id, ac_ups_title, ac_ups_type, ac_ups_desc, ac_ups_ipname, ac_tin, ac_ups_sc1, ac_ups_sched1done, ac_ip_loi, ac_ups_aloi, ac_ups_con, ac_ip_fb1, ac_ip_fbd1, ac_ip_fb2, ac_ip_fbd2, ac_ip_fb3, ac_ip_fbd3, ac_ip_doc1, ac_ip_docd1, ac_ip_doc2, ac_ip_docd2, ac_ip_doc3, ac_ip_docd3, ac_ups_fb1, ac_ups_fbd1, ac_ups_fb2, ac_ups_fbd2, ac_ups_fb3, ac_ups_fbd3, ac_ups_doc1, ac_ups_docd1, ac_ups_doc2, ac_ups_docd2, ac_ups_doc3, ac_ups_docd3, ac_ip_final, ac_ups_final, ac_ups_meet, ac_ups_meetd, ac_ovpla_sign, ac_ovpla_docfin, ac_ovpla_docfind, ac_tout, ac_percent, ac_delete) VALUES (1, 'Apple x UPSCALE New iPhone Manufacturing Plant', 'Licensing', 'A collaboration of Apple to UPSCALE to make a production facility in the Philippines', 'Apple Inc.', '2024-05-30 17:38:47', '', false, NULL, false, NULL, NULL, false, NULL, false, NULL, false, NULL, false, NULL, false, NULL, false, NULL, false, NULL, false, NULL, false, NULL, false, NULL, false, NULL, false, NULL, 'false', NULL, false, NULL, NULL, NULL, NULL, '0.12', false);


--
-- TOC entry 3382 (class 0 OID 57475)
-- Dependencies: 219
-- Data for Name: indpartners; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.indpartners (ip_id, ip_name, ip_ind, ip_person, ip_phone, ip_email, ip_add, ip_upd, ip_remarks, ip_delete) VALUES (1, 'Apple Inc.', 'Tech Devices', 'Steve Jobs', '09379582942', 'imapple@gmail.com', '2024-05-15 10:29:50', '2024-05-15 10:30:26', 'Reliable and fast to reach', false);
INSERT INTO public.indpartners (ip_id, ip_name, ip_ind, ip_person, ip_phone, ip_email, ip_add, ip_upd, ip_remarks, ip_delete) VALUES (2, 'Jollibee Foods Corporation', 'Food & Beverages', 'Joshua Caktiong', '0936392944', 'jollibeebirthday@gmail.com', '2024-05-16 15:06:40', '2024-05-16 15:06:40', '', false);


--
-- TOC entry 3380 (class 0 OID 57453)
-- Dependencies: 217
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users (user_id, user_fname, user_lname, user_email, user_cname, user_pwd, user_access, user_crt, user_lastupd, user_delete, user_r1, user_r2, user_r3, user_r4, user_r5, user_r6, user_r7, user_r8, user_r9, user_r10) VALUES (3, 'Luis', 'Sison', 'lsison@gmail.com', 'ls001', 'fcdd80dc9afe93a4243372d1fd4f74e4649110ca5332420261d237488d47e48f', 'Admin', '2024-06-19 16:30:34.302474', '2024-06-19 16:30:34.302474', false, false, false, false, false, false, false, false, false, false, false);
INSERT INTO public.users (user_id, user_fname, user_lname, user_email, user_cname, user_pwd, user_access, user_crt, user_lastupd, user_delete, user_r1, user_r2, user_r3, user_r4, user_r5, user_r6, user_r7, user_r8, user_r9, user_r10) VALUES (4, 'admin', 'Admin', 'admin@gmail.com', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Admin', '2024-06-19 16:35:52.073266', '2024-06-19 16:35:52.073266', false, false, false, false, false, false, false, false, false, false, false);
INSERT INTO public.users (user_id, user_fname, user_lname, user_email, user_cname, user_pwd, user_access, user_crt, user_lastupd, user_delete, user_r1, user_r2, user_r3, user_r4, user_r5, user_r6, user_r7, user_r8, user_r9, user_r10) VALUES (2, 'a', 'a', 'a', 'a', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'Admin', '2024-06-19 16:30:07.81149', '2024-06-19 16:30:07.81149', true, false, false, false, false, false, false, false, false, false, false);


--
-- TOC entry 3392 (class 0 OID 0)
-- Dependencies: 214
-- Name: contracts_ac_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contracts_ac_id_seq', 1, true);


--
-- TOC entry 3393 (class 0 OID 0)
-- Dependencies: 218
-- Name: indpartners_ip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.indpartners_ip_id_seq', 2, true);


--
-- TOC entry 3394 (class 0 OID 0)
-- Dependencies: 216
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 4, true);


--
-- TOC entry 3230 (class 2606 OID 57451)
-- Name: contracts contracts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_pkey PRIMARY KEY (ac_id);


--
-- TOC entry 3234 (class 2606 OID 57484)
-- Name: indpartners indpartners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.indpartners
    ADD CONSTRAINT indpartners_pkey PRIMARY KEY (ip_id);


--
-- TOC entry 3232 (class 2606 OID 57471)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


-- Completed on 2024-06-27 23:10:03

--
-- PostgreSQL database dump complete
--

