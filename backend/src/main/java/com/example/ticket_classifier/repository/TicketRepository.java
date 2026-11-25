package com.example.ticket_classifier.repository;

import com.example.ticket_classifier.entity.Ticket;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import org.springframework.data.domain.Sort;
import TicketStatus;

public interface TicketRepository extends JpaRepository<Ticket,Long> {

    List<Ticket> findByStatus(TicketStatus status, Sort sort);
}
