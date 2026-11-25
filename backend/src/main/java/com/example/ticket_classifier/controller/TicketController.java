package com.example.ticket_classifier.controller;

import com.example.ticket_classifier.dto.CreateTicketRequest;
import com.example.ticket_classifier.dto.UpdateTicketStatusRequest;
import com.example.ticket_classifier.entity.Ticket;
import com.example.ticket_classifier.service.TicketService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/tickets")
public class TicketController {

    private final TicketService ticketService;

    public TicketController(TicketService ticketService) {
        this.ticketService = ticketService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Ticket create(@RequestBody CreateTicketRequest request) {
        return ticketService.create(request);
    }

    @GetMapping
    public List<Ticket> getAll() {
        return ticketService.getAll();
    }

    @GetMapping("/{id}")
    public Ticket getById(@PathVariable Long id) {
        return ticketService.getById(id);
    }

    @PatchMapping("/{id}/status")
    public Ticket updateStatus(@PathVariable Long id, @RequestBody UpdateTicketStatusRequest request) {
        return ticketService.updateStatus(id, request.getStatus());
    }
}