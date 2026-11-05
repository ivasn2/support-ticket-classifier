package com.example.ticket_classifier.repository;

import com.example.ticket_classifier.entity.Ticket;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TicketRepository extends JpaRepository<Ticket,Long> {
}
