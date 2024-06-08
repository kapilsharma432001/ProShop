import React, { useEffect } from "react";
import { Link, useNavigate, useParams, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import {
  Row,
  Col,
  ListGroup,
  Image,
  Form,
  Button,
  Card,
} from "react-bootstrap";
import Message from "../components/Message";
import { addToCart } from "../actions/cartActions";

function CartScreen() {
  const { id } = useParams();
  const location = useLocation();
  const qty = new URLSearchParams(location.search)
    ? Number(new URLSearchParams(location.search).get("qty"))
    : 1;

  const dispatch = useDispatch();
  const cart = useSelector((state) => state.cart);
  const { cartItems } = cart;
  console.log("Cart Items: ", cartItems);
  useEffect(() => {
    if (id) {
      dispatch(addToCart(id, qty));
    }
  }, [dispatch, id, qty]);

  console.log("Qty: ", qty, "Product Id: ", id);
}

export default CartScreen;
