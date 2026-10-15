"""Tests must mock external services instead of opening network sockets."""

import socket

import pytest
from pytest_socket import SocketBlockedError


@pytest.mark.parametrize("family", [socket.AF_INET, socket.AF_INET6])
def test_network_sockets_are_blocked(family: socket.AddressFamily) -> None:
    with pytest.raises(SocketBlockedError):
        socket.socket(family, socket.SOCK_STREAM)
